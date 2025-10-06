from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.api.schemas import AskRequest, AskResponse
from src.services import gemini_client
from src.database import get_db
from src.database.crud import create_qa

router = APIRouter(prefix="/ask", tags=["AI Q&A"])

# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=AskResponse,
    summary="Ask a question to the AI",
    description="Submit a question and receive an AI-generated answer. The question and answer are persisted to the database.",
    responses={
        200: {
            "description": "Successful response with AI answer",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "This is the AI-generated answer to your question.",
                        "id": 1,
                        "timestamp": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        400: {"description": "Bad request - invalid input"},
        500: {"description": "Internal server error"},
        502: {"description": "Bad gateway - Gemini API call failed"}
    }
)
def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db)
) -> AskResponse:
    """
    Process a user question and return an AI-generated answer.
    
    This endpoint:
    1. Validates the incoming question
    2. Calls the Gemini API to generate an answer
    3. Persists both question and answer to the database
    4. Returns the answer along with metadata
    
    Args:
        request: AskRequest containing the user's question
        db: Database session (injected dependency)
    
    Returns:
        AskResponse: Contains the answer, database ID, and timestamp
        
    Raises:
        HTTPException: 400 for validation errors, 502 for Gemini API failures, 500 for other errors
    """
    try:
        # Validate question
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        # Call Gemini API to generate answer
        try:
            answer = gemini_client.generate_answer(request.question)
        except Exception as gemini_error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to get response from AI service: {str(gemini_error)}"
            )
        
        # Persist to database
        try:
            qa_record = create_qa(db, request.question, answer)
        except Exception as db_error:
            # Log the error but still return the answer
            # In production, you might want to handle this differently
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save to database: {str(db_error)}"
            )
        
        # Return response
        return AskResponse(
            answer=qa_record.answer,
            id=qa_record.id,
            timestamp=qa_record.created_at
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
