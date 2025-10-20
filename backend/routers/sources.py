from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime, timezone
from models import Source, SourceCreate, SourceResponse
from auth import get_current_user, get_mock_user, User
from services.document_processor import DocumentProcessor
from services.website_scraper import WebsiteScraper
from services.plan_service import plan_service
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sources", tags=["sources"])
db_instance = None


def init_router(db: AsyncIOMotorDatabase):
    """Initialize router with database instance"""
    global db_instance
    db_instance = db


async def verify_chatbot_ownership(chatbot_id: str, user_id: str):
    """Verify that the chatbot belongs to the user"""
    chatbot = await db_instance.chatbots.find_one({
        "id": chatbot_id,
        "user_id": user_id
    })
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    return chatbot


@router.get("/chatbot/{chatbot_id}", response_model=List[SourceResponse])
async def get_sources(
    chatbot_id: str,
    current_user: User = Depends(get_mock_user)
):
    """Get all sources for a chatbot"""
    try:
        # Verify ownership
        await verify_chatbot_ownership(chatbot_id, current_user.id)
        
        sources = await db_instance.sources.find(
            {"chatbot_id": chatbot_id}
        ).to_list(length=None)
        
        return [SourceResponse(**source) for source in sources]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching sources: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch sources"
        )


@router.post("/chatbot/{chatbot_id}/file", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def upload_file_source(
    chatbot_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_mock_user)
):
    """Upload a file as a training source (max 100MB)"""
    try:
        # Verify ownership
        await verify_chatbot_ownership(chatbot_id, current_user.id)
        
        # Read file content
        file_content = await file.read()
        file_size = len(file_content)
        
        # Check file size limit (100MB)
        MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of 100MB. Current size: {DocumentProcessor.format_size(file_size)}"
            )
        
        # Create source entry
        source = Source(
            chatbot_id=chatbot_id,
            type="file",
            name=file.filename,
            size=DocumentProcessor.format_size(file_size),
            status="processing"
        )
        
        await db_instance.sources.insert_one(source.model_dump())
        
        # Process file in background
        async def process_file():
            try:
                content = DocumentProcessor.process_file(file.filename, file_content)
                
                await db_instance.sources.update_one(
                    {"id": source.id},
                    {"$set": {
                        "content": content,
                        "status": "processed"
                    }}
                )
                
                # Update chatbot last_trained timestamp
                await db_instance.chatbots.update_one(
                    {"id": chatbot_id},
                    {"$set": {"last_trained": datetime.now(timezone.utc)}}
                )
            except Exception as e:
                logger.error(f"Error processing file: {str(e)}")
                await db_instance.sources.update_one(
                    {"id": source.id},
                    {"$set": {
                        "status": "failed",
                        "error_message": str(e)
                    }}
                )
        
        # Start background task
        asyncio.create_task(process_file())
        
        return SourceResponse(**source.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file"
        )


@router.post("/chatbot/{chatbot_id}/website", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def add_website_source(
    chatbot_id: str,
    url: str = Form(...),
    current_user: User = Depends(get_mock_user)
):
    """Add a website as a training source"""
    try:
        # Verify ownership
        await verify_chatbot_ownership(chatbot_id, current_user.id)
        
        # Create source entry
        source = Source(
            chatbot_id=chatbot_id,
            type="website",
            name=url,
            url=url,
            status="processing"
        )
        
        await db_instance.sources.insert_one(source.model_dump())
        
        # Scrape website in background
        async def scrape_website():
            try:
                content = WebsiteScraper.scrape_url(url)
                
                await db_instance.sources.update_one(
                    {"id": source.id},
                    {"$set": {
                        "content": content,
                        "status": "processed"
                    }}
                )
                
                # Update chatbot last_trained timestamp
                await db_instance.chatbots.update_one(
                    {"id": chatbot_id},
                    {"$set": {"last_trained": datetime.now(timezone.utc)}}
                )
            except Exception as e:
                logger.error(f"Error scraping website: {str(e)}")
                await db_instance.sources.update_one(
                    {"id": source.id},
                    {"$set": {
                        "status": "failed",
                        "error_message": str(e)
                    }}
                )
        
        # Start background task
        asyncio.create_task(scrape_website())
        
        return SourceResponse(**source.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding website: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add website"
        )


@router.post("/chatbot/{chatbot_id}/text", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def add_text_source(
    chatbot_id: str,
    name: str = Form(...),
    content: str = Form(...),
    current_user: User = Depends(get_mock_user)
):
    """Add text content as a training source"""
    try:
        # Verify ownership
        await verify_chatbot_ownership(chatbot_id, current_user.id)
        
        # Create source entry
        source = Source(
            chatbot_id=chatbot_id,
            type="text",
            name=name,
            content=content,
            status="processed"
        )
        
        await db_instance.sources.insert_one(source.model_dump())
        
        # Update chatbot last_trained timestamp
        await db_instance.chatbots.update_one(
            {"id": chatbot_id},
            {"$set": {"last_trained": datetime.now(timezone.utc)}}
        )
        
        return SourceResponse(**source.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding text: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add text"
        )


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: str,
    current_user: User = Depends(get_mock_user)
):
    """Delete a source"""
    try:
        # Get source
        source = await db_instance.sources.find_one({"id": source_id})
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found"
            )
        
        # Verify ownership through chatbot
        await verify_chatbot_ownership(source["chatbot_id"], current_user.id)
        
        # Delete source
        await db_instance.sources.delete_one({"id": source_id})
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting source: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete source"
        )
