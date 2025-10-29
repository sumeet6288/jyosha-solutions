import logging
from typing import List, Dict, Optional
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import TEXT
import re
from collections import Counter
import math

logger = logging.getLogger(__name__)


class VectorStore:
    """Service for managing document chunks using MongoDB with basic text search"""
    
    def __init__(self):
        """Initialize MongoDB connection for chunk storage"""
        try:
            # Get MongoDB connection string
            mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
            db_name = os.environ.get('MONGO_DB_NAME', 'botsmith')
            
            # Initialize MongoDB client
            self.client = AsyncIOMotorClient(mongo_url)
            self.db = self.client[db_name]
            self.chunks_collection = self.db['document_chunks']
            
            logger.info(f"MongoDB VectorStore initialized with database: {db_name}")
            
        except Exception as e:
            logger.error(f"Error initializing MongoDB VectorStore: {str(e)}")
            raise Exception(f"Failed to initialize vector store: {str(e)}")
    
    def get_or_create_collection(self, chatbot_id: str):
        """
        Get or create a collection for a specific chatbot
        
        Args:
            chatbot_id: Unique identifier for the chatbot
            
        Returns:
            ChromaDB collection object
        """
        try:
            # Collection name must be alphanumeric with underscores/hyphens
            collection_name = f"chatbot_{chatbot_id}".replace("-", "_")
            
            # Get or create collection
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"chatbot_id": chatbot_id}
            )
            
            logger.info(f"Collection '{collection_name}' ready with {collection.count()} items")
            return collection
            
        except Exception as e:
            logger.error(f"Error getting/creating collection: {str(e)}")
            raise Exception(f"Failed to get collection: {str(e)}")
    
    async def add_chunks(
        self,
        chatbot_id: str,
        chunks: List[Dict],
        embeddings: List[List[float]],
        source_id: str,
        source_type: str,
        filename: str = None
    ) -> Dict:
        """
        Add document chunks with embeddings to vector store
        
        Args:
            chatbot_id: Chatbot identifier
            chunks: List of chunk dictionaries with text and metadata
            embeddings: List of embedding vectors
            source_id: Source document identifier
            source_type: Type of source (file, website, text)
            filename: Optional filename for file sources
            
        Returns:
            Dictionary with operation statistics
        """
        try:
            if len(chunks) != len(embeddings):
                raise ValueError(f"Chunks ({len(chunks)}) and embeddings ({len(embeddings)}) count mismatch")
            
            collection = self.get_or_create_collection(chatbot_id)
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            embeddings_list = embeddings
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                # Create unique ID for chunk
                chunk_id = f"{source_id}_chunk_{i}"
                ids.append(chunk_id)
                
                # Extract text
                documents.append(chunk["text"])
                
                # Prepare metadata
                metadata = {
                    "source_id": source_id,
                    "source_type": source_type,
                    "chunk_index": chunk.get("chunk_index", i),
                    "token_count": chunk.get("token_count", 0)
                }
                
                if filename:
                    metadata["filename"] = filename
                
                # Add any additional metadata from chunk
                if "page" in chunk:
                    metadata["page"] = chunk["page"]
                
                metadatas.append(metadata)
            
            # Add to ChromaDB
            collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings_list
            )
            
            logger.info(f"Added {len(chunks)} chunks to collection for chatbot {chatbot_id}")
            
            return {
                "success": True,
                "chunks_added": len(chunks),
                "collection_size": collection.count()
            }
            
        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {str(e)}")
            raise Exception(f"Failed to add chunks: {str(e)}")
    
    async def search(
        self,
        chatbot_id: str,
        query_embedding: List[float],
        top_k: int = 5,
        min_similarity: float = 0.7
    ) -> List[Dict]:
        """
        Search for similar chunks using vector similarity
        
        Args:
            chatbot_id: Chatbot identifier
            query_embedding: Query embedding vector
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            List of dictionaries with matched chunks and metadata
        """
        try:
            collection = self.get_or_create_collection(chatbot_id)
            
            # Check if collection has any documents
            if collection.count() == 0:
                logger.info(f"Collection for chatbot {chatbot_id} is empty")
                return []
            
            # Search using cosine similarity
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Process results
            matches = []
            
            if results and results["documents"] and len(results["documents"][0]) > 0:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    # Convert distance to similarity score (ChromaDB uses L2 distance)
                    # For normalized vectors: similarity = 1 - (distance^2 / 2)
                    similarity = max(0, 1 - (distance ** 2) / 2)
                    
                    # Filter by minimum similarity
                    if similarity >= min_similarity:
                        matches.append({
                            "text": doc,
                            "metadata": metadata,
                            "similarity": round(similarity, 4),
                            "rank": i + 1
                        })
            
            logger.info(f"Found {len(matches)} matches above {min_similarity} similarity for chatbot {chatbot_id}")
            return matches
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    async def delete_source(self, chatbot_id: str, source_id: str) -> Dict:
        """
        Delete all chunks associated with a source
        
        Args:
            chatbot_id: Chatbot identifier
            source_id: Source identifier
            
        Returns:
            Dictionary with deletion statistics
        """
        try:
            collection = self.get_or_create_collection(chatbot_id)
            
            # Get all chunks for this source
            results = collection.get(
                where={"source_id": source_id},
                include=["metadatas"]
            )
            
            if results and results["ids"]:
                # Delete chunks
                collection.delete(ids=results["ids"])
                deleted_count = len(results["ids"])
                
                logger.info(f"Deleted {deleted_count} chunks for source {source_id}")
                
                return {
                    "success": True,
                    "chunks_deleted": deleted_count,
                    "collection_size": collection.count()
                }
            else:
                logger.info(f"No chunks found for source {source_id}")
                return {
                    "success": True,
                    "chunks_deleted": 0,
                    "collection_size": collection.count()
                }
                
        except Exception as e:
            logger.error(f"Error deleting source from vector store: {str(e)}")
            raise Exception(f"Failed to delete source: {str(e)}")
    
    async def delete_chatbot_collection(self, chatbot_id: str) -> bool:
        """
        Delete entire collection for a chatbot
        
        Args:
            chatbot_id: Chatbot identifier
            
        Returns:
            True if successful
        """
        try:
            collection_name = f"chatbot_{chatbot_id}".replace("-", "_")
            self.client.delete_collection(name=collection_name)
            logger.info(f"Deleted collection {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False
    
    def get_collection_stats(self, chatbot_id: str) -> Dict:
        """Get statistics about a collection"""
        try:
            collection = self.get_or_create_collection(chatbot_id)
            
            return {
                "total_chunks": collection.count(),
                "collection_name": collection.name,
                "metadata": collection.metadata
            }
            
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"total_chunks": 0, "error": str(e)}
