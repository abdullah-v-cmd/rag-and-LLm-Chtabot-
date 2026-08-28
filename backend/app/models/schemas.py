"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    use_rag: bool = Field(True, description="Whether to use RAG for context")
    max_tokens: Optional[int] = Field(500, ge=50, le=2000)
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    """Chat response model."""
    message: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="Source documents used")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DocumentUploadResponse(BaseModel):
    """Document upload response model."""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    processed: bool = Field(..., description="Whether document was processed")
    chunks_created: Optional[int] = Field(None, description="Number of text chunks created")
    message: str = Field(..., description="Status message")


class DocumentInfo(BaseModel):
    """Document information model."""
    document_id: str
    filename: str
    file_size: int
    upload_date: datetime
    processed: bool
    chunks_count: Optional[int] = None


class DocumentListResponse(BaseModel):
    """Document list response model."""
    documents: List[DocumentInfo]
    total: int


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment")
    timestamp: datetime = Field(..., description="Current timestamp")
    services: Dict[str, bool] = Field(..., description="Status of dependent services")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error detail message")
    status: str = Field(default="error", description="Status indicator")
    error_code: Optional[str] = Field(None, description="Specific error code")
