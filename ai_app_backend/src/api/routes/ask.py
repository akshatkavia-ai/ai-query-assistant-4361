"""
API routes for the /ask endpoint.

Handles question answering requests using Gemini AI and persists Q&A history.
"""

import logging
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import AskRequest, AskResponse, ErrorResponse
from src.services.gemini_service import get_gemini_service, GeminiService
from src.database.connection import SessionLocal
from src.database.models import QAHistory

# Configure logging
logger = logging.getLogger(__name__)

# Create router with tags for API documentation
router = APIRouter(
    prefix="",
    tags=["Question Answering"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)


def get_optional_db_session() -> Optional[Session]:
    """
    Get database session if available, otherwise return None.
    
    This allows the endpoint to function without database connectivity.
    
    Returns:
        Optional[Session]: Database session or None if database is not configured
    """
    if SessionLocal is None:
        logger.warning("Database not configured, skipping database operations")
        return None
    
    try:
        db = SessionLocal()
        return db
    except Exception as e:
        logger.error(f"Failed to create database session: {e}")
        return None


# PUBLIC_INTERFACE
@router.post(
    "/ask",
    response_model=AskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a question to the AI assistant",
    description="""
    Submit a question to the AI assistant and receive an answer.
    
    The question is processed by Google Gemini AI, and both the question
    and answer are stored in the database for history tracking.
    
    **Parameters:**
    - **question**: The question to ask (1-5000 characters, cannot be empty)
    
    **Returns:**
    - **answer**: The AI-generated answer
    - **id**: Database ID of the stored Q&A record
    - **created_at**: ISO timestamp of when the answer was created
    
    **Error Responses:**
    - **400**: Invalid request (e.g., empty question)
    - **500**: Internal server error
    - **503**: AI service unavailable
    """
)
async def ask_question(
    request: AskRequest,
    gemini: GeminiService = Depends(get_gemini_service)
):
    """
    Process a question and return an AI-generated answer.
    
    Args:
        request: AskRequest containing the question
        gemini: Gemini service instance (injected)
        
    Returns:
        AskResponse: Contains answer, id, and created_at timestamp
        
    Raises:
        HTTPException: If validation fails or service is unavailable
    """
    db = None
    try:
        # Validate that Gemini service is available
        if not gemini.is_available():
            logger.error("Gemini service is not available")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service is not available. Please ensure GEMINI_API_KEY is configured."
            )
        
        # Log incoming request
        logger.info(f"Received question: {request.question[:100]}...")
        
        # Generate answer using Gemini
        try:
            answer = gemini.generate_answer(request.question)
        except ValueError as ve:
            logger.error(f"Configuration error: {ve}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(ve)
            )
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate answer: {str(e)}"
            )
        
        # Try to get database session (optional)
        db = get_optional_db_session()
        
        # Persist Q&A to database if available
        qa_id = None
        created_at = datetime.utcnow()
        
        if db is not None:
            try:
                qa_record = QAHistory(
                    question=request.question,
                    answer=answer
                )
                db.add(qa_record)
                db.commit()
                db.refresh(qa_record)
                
                qa_id = qa_record.id
                created_at = qa_record.created_at
                
                logger.info(f"✓ Q&A record saved with ID: {qa_record.id}")
                
            except Exception as e:
                logger.warning(f"⚠ Database error (non-fatal): {e}")
                db.rollback()
                # Don't fail the request, just log the warning
                logger.info("Continuing without database persistence")
        else:
            logger.warning("⚠ Database not available, skipping persistence")
        
        # Return response (with or without database ID)
        return AskResponse(
            answer=answer,
            id=qa_id if qa_id is not None else 0,
            created_at=created_at.isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"✗ Unexpected error in ask_question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
    finally:
        # Clean up database session if it was created
        if db is not None:
            try:
                db.close()
            except Exception:
                pass
