from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from .connection import Base

class QAHistory(Base):
    """
    Model for storing question and answer history.
    
    Attributes:
        id: Primary key
        question: User's question text
        answer: AI-generated answer text
        created_at: Timestamp when the QA pair was created
    """
    __tablename__ = 'qa_history'
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
