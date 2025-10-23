from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime, timezone, date
import uuid


# User Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Chatbot Models
class Chatbot(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    status: Literal["active", "inactive"] = "active"
    model: str = "gpt-4o-mini"  # Default model
    provider: str = "openai"  # openai, anthropic, gemini
    temperature: float = 0.7
    instructions: str = "You are a helpful assistant."
    welcome_message: str = "Hello! How can I help you today?"
    conversations_count: int = 0
    messages_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_trained: Optional[datetime] = None
    
    # Customization fields
    primary_color: str = "#7c3aed"  # Default purple
    secondary_color: str = "#a78bfa"  # Light purple
    accent_color: str = "#ec4899"  # Default pink
    logo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    widget_position: Literal["bottom-right", "bottom-left", "top-right", "top-left"] = "bottom-right"
    widget_theme: Literal["light", "dark", "auto"] = "light"
    
    # New appearance features
    font_family: str = "Inter, system-ui, sans-serif"
    font_size: Literal["small", "medium", "large"] = "medium"
    bubble_style: Literal["rounded", "square", "smooth"] = "rounded"
    widget_size: Literal["small", "medium", "large"] = "medium"
    auto_expand: bool = False
    
    # Sharing & Integration
    public_access: bool = False
    webhook_url: Optional[str] = None
    webhook_enabled: bool = False


class ChatbotCreate(BaseModel):
    name: str
    model: str = "gpt-4o-mini"
    provider: str = "openai"
    temperature: float = 0.7
    instructions: str = "You are a helpful assistant."
    welcome_message: str = "Hello! How can I help you today?"
    primary_color: str = "#7c3aed"
    secondary_color: str = "#a78bfa"
    logo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    widget_position: Literal["bottom-right", "bottom-left", "top-right", "top-left"] = "bottom-right"
    widget_theme: Literal["light", "dark", "auto"] = "light"


class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = None
    instructions: Optional[str] = None
    welcome_message: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    widget_position: Optional[Literal["bottom-right", "bottom-left", "top-right", "top-left"]] = None
    widget_theme: Optional[Literal["light", "dark", "auto"]] = None
    public_access: Optional[bool] = None
    webhook_url: Optional[str] = None
    webhook_enabled: Optional[bool] = None


class ChatbotResponse(BaseModel):
    id: str
    user_id: str
    name: str
    status: str
    model: str
    provider: str
    temperature: float
    instructions: str
    welcome_message: str
    conversations_count: int
    messages_count: int
    created_at: datetime
    updated_at: datetime
    last_trained: Optional[datetime] = None
    primary_color: str = "#7c3aed"
    secondary_color: str = "#a78bfa"
    logo_url: Optional[str] = None
    avatar_url: Optional[str] = None
    widget_position: str = "bottom-right"
    widget_theme: str = "light"
    public_access: bool = False
    webhook_url: Optional[str] = None
    webhook_enabled: bool = False


# Source Models
class Source(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chatbot_id: str
    type: Literal["file", "website", "text"]
    name: str
    content: str = ""  # Processed/extracted content
    size: Optional[str] = None  # For files
    url: Optional[str] = None  # For websites
    status: Literal["processing", "processed", "failed"] = "processing"
    error_message: Optional[str] = None
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SourceCreate(BaseModel):
    type: Literal["file", "website", "text"]
    name: str
    content: Optional[str] = None
    url: Optional[str] = None


class SourceResponse(BaseModel):
    id: str
    chatbot_id: str
    type: str
    name: str
    size: Optional[str] = None
    url: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    added_at: datetime


# Conversation Models
class Conversation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chatbot_id: str
    session_id: str  # For tracking user sessions
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    status: Literal["active", "resolved", "escalated"] = "active"
    messages_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationResponse(BaseModel):
    id: str
    chatbot_id: str
    session_id: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    status: str
    messages_count: int
    created_at: datetime
    updated_at: datetime


# Message Models
class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    chatbot_id: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    chatbot_id: str
    role: str
    content: str
    timestamp: datetime


# Chat Request/Response
class ChatRequest(BaseModel):
    chatbot_id: str
    message: str
    session_id: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    session_id: str


# Analytics Models
class Analytics(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    chatbot_id: str
    date: date
    total_conversations: int = 0
    total_messages: int = 0
    active_chats: int = 0
    avg_response_time: float = 0.0
    satisfaction_rate: float = 0.0


class DashboardAnalytics(BaseModel):
    total_conversations: int
    total_messages: int
    active_chatbots: int
    total_chatbots: int


class ChatbotAnalytics(BaseModel):
    chatbot_id: str
    total_conversations: int
    total_messages: int
    date_range: List[date]
    conversations_by_date: dict
    messages_by_date: dict



# Conversation Rating Models
class ConversationRating(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    chatbot_id: str
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    feedback: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RatingCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None


class RatingResponse(BaseModel):
    id: str
    conversation_id: str
    rating: int
    feedback: Optional[str]
    created_at: datetime


# Advanced Analytics Models
class TrendDataPoint(BaseModel):
    date: str
    conversations: int
    messages: int


class TrendAnalytics(BaseModel):
    chatbot_id: str
    period: str  # 7days, 30days, 90days
    data: List[TrendDataPoint]
    total_conversations: int
    total_messages: int
    avg_daily_conversations: float
    avg_daily_messages: float


class TopQuestion(BaseModel):
    question: str
    count: int
    percentage: float


class TopQuestionsAnalytics(BaseModel):
    chatbot_id: str
    top_questions: List[TopQuestion]
    total_unique_questions: int


class SatisfactionAnalytics(BaseModel):
    chatbot_id: str
    average_rating: float
    total_ratings: int
    rating_distribution: dict  # {1: count, 2: count, ...}
    satisfaction_percentage: float  # % of 4-5 star ratings


class PerformanceMetrics(BaseModel):
    chatbot_id: str
    avg_response_time_ms: float
    total_responses: int
    fastest_response_ms: float
    slowest_response_ms: float


# Public Chat Models
class PublicChatbotInfo(BaseModel):
    id: str
    name: str
    welcome_message: str
    primary_color: str
    secondary_color: str
    logo_url: Optional[str]
    avatar_url: Optional[str]
    widget_theme: str


class PublicChatRequest(BaseModel):
    message: str
    session_id: str
    user_name: Optional[str] = None
    user_email: Optional[str] = None


# Embed Code Models
class EmbedConfig(BaseModel):
    chatbot_id: str
    theme: str = "light"
    position: str = "bottom-right"


class EmbedCodeResponse(BaseModel):
    html_code: str
    script_url: str



# Plan and Subscription Models
class PlanLimits(BaseModel):
    """Plan usage limits"""
    max_chatbots: int = Field(description="Maximum number of chatbots")
    max_messages_per_month: int = Field(description="Maximum messages per month")
    max_file_uploads: int = Field(description="Maximum file uploads")
    max_file_size_mb: int = Field(description="Maximum file size in MB")
    max_website_sources: int = Field(description="Maximum website sources")
    max_text_sources: int = Field(description="Maximum text sources")
    conversation_history_days: int = Field(description="Days to keep conversation history")
    allowed_ai_providers: List[str] = Field(default=["openai"], description="Allowed AI providers")
    api_access: bool = Field(default=False, description="API access enabled")
    custom_branding: bool = Field(default=False, description="Custom branding enabled")
    analytics_level: str = Field(default="basic", description="Analytics level: basic or advanced")
    support_level: str = Field(default="community", description="Support level")


class Plan(BaseModel):
    """Subscription plan model"""
    id: str = Field(description="Plan ID (free, starter, professional, enterprise)")
    name: str = Field(description="Plan name")
    price: float = Field(description="Monthly price in USD (0 for free, -1 for custom)")
    description: str = Field(description="Plan description")
    limits: PlanLimits = Field(description="Plan limits")
    features: List[str] = Field(default=[], description="Plan features list")
    is_active: bool = Field(default=True, description="Is plan active")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlanUpgradeRequest(BaseModel):
    """Plan upgrade request"""
    new_plan_id: str = Field(description="ID of the plan to upgrade to")

