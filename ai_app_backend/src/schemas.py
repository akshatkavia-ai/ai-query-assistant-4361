"""
Pydantic schemas for API request/response validation.

Defines data models for API endpoints with automatic validation.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator


class AskRequest(BaseModel):
    """
    Schema for POST /ask request body.
    
    Attributes:
        question: The user's question to ask the AI
    """
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The question to ask the AI assistant"
    )
    
    @validator('question')
    def validate_question(cls, v):
        """Validate that question is not just whitespace."""
        if not v.strip():
            raise ValueError("Question cannot be empty or only whitespace")
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the capital of France?"
            }
        }


class AskResponse(BaseModel):
    """
    Schema for POST /ask response.
    
    Attributes:
        answer: The AI-generated answer
        id: Database ID of the stored Q&A record
        created_at: Timestamp when the answer was generated
    """
    answer: str = Field(
        ...,
        description="The AI-generated answer to the question"
    )
    id: int = Field(
        ...,
        description="Unique identifier for this Q&A record"
    )
    created_at: str = Field(
        ...,
        description="ISO format timestamp of when the answer was created"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The capital of France is Paris.",
                "id": 1,
                "created_at": "2024-01-15T10:30:00+00:00"
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    Attributes:
        error: Error message
        detail: Optional detailed error information
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Service unavailable",
                "detail": "Unable to connect to AI service"
            }
        }
