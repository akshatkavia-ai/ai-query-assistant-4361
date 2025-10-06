from sqlalchemy.orm import Session
from .models import QAHistory

# PUBLIC_INTERFACE
def create_qa(db: Session, question: str, answer: str) -> QAHistory:
    """
    Create a new QA history record.
    
    Args:
        db: Database session
        question: User's question text
        answer: AI-generated answer text
    
    Returns:
        QAHistory: Created database record
    """
    row = QAHistory(question=question, answer=answer)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

# PUBLIC_INTERFACE
def list_qa(db: Session, limit: int = 20):
    """
    Retrieve recent QA history records.
    
    Args:
        db: Database session
        limit: Maximum number of records to return (default: 20)
    
    Returns:
        list[QAHistory]: List of QA history records ordered by most recent
    """
    return db.query(QAHistory).order_by(QAHistory.id.desc()).limit(limit).all()
