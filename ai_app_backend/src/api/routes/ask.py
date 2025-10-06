"""
API routes for the /ask endpoint.

Handles question answering requests using Gemini AI and persists Q&A history.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schemas import AskRequest, AskResponse, ErrorResponse
from src.services.gemini_service import get_gemini_service, GeminiService
from src.database.connection import get_db_session
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
    db: Session = Depends(get_db_session),
    gemini: GeminiService = Depends(get_gemini_service)
):
    """
    Process a question and return an AI-generated answer.
    
    Args:
        request: AskRequest containing the question
        db: Database session (injected)
        gemini: Gemini service instance (injected)
        
    Returns:
        AskResponse: Contains answer, id, and created_at timestamp
        
    Raises:
        HTTPException: If validation fails or service is unavailable
    """
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
        
        # Persist Q&A to database
        try:
            qa_record = QAHistory(
                question=request.question,
                answer=answer
            )
            db.add(qa_record)
            db.commit()
            db.refresh(qa_record)
            
            logger.info(f"✓ Q&A record saved with ID: {qa_record.id}")
            
        except Exception as e:
            logger.error(f"✗ Database error: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save Q&A record to database"
            )
        
        # Return response
        return AskResponse(
            answer=answer,
            id=qa_record.id,
            created_at=qa_record.created_at.isoformat()
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
