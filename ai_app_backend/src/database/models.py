"""
Database ORM models.

Defines SQLAlchemy models for database tables.
"""

from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from src.database.connection import Base


class QAHistory(Base):
    """
    Model for storing question and answer history.
    
    Attributes:
        id: Primary key (serial)
        question: User's question text
        answer: AI-generated answer text
        created_at: Timestamp when the Q&A pair was created
    """
    __tablename__ = "qa_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self):
        """String representation of QAHistory instance."""
        return f"<QAHistory(id={self.id}, question='{self.question[:50]}...', created_at={self.created_at})>"
    
    def to_dict(self):
        """
        Convert model instance to dictionary.
        
        Returns:
            dict: Dictionary representation of the Q&A record
        """
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
