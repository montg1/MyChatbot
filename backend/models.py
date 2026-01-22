"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, description="User's message/question")
    sessionId: str = Field(..., min_length=1, description="Session ID for context")
    history: Optional[List[ChatMessage]] = Field(
        default=[],
        description="Previous messages for conversation context"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is your experience with Python?",
                "sessionId": "abc123-def456",
                "history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi! How can I help you?"}
                ]
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reply: str = Field(..., description="AI-generated response")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(default="healthy", description="Service health status")
