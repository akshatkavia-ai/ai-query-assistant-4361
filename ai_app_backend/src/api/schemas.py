from pydantic import BaseModel, Field
from datetime import datetime

class AskRequest(BaseModel):
    """
    Request schema for asking a question to the AI.
    
    Attributes:
        question: The user's question text
    """
    question: str = Field(..., min_length=1, description="The question to ask the AI")

class AskResponse(BaseModel):
    """
    Response schema for AI answer.
    
    Attributes:
        answer: The AI-generated answer
        id: Database record ID
        timestamp: When the QA pair was created
    """
    answer: str = Field(..., description="The AI-generated answer")
    id: int = Field(..., description="Database record ID")
    timestamp: datetime = Field(..., description="Timestamp of the QA record")
    
    class Config:
        from_attributes = True
