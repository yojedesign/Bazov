"""
Signal database model
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from typing import Optional
from datetime import datetime

from app.db.base import BaseModel


class Signal(BaseModel):
    """
    Signal model for business signals (hiring, funding, partnerships, etc.)
    """
    
    __tablename__ = "signals"
    
    # Signal type
    signal_type = Column(String(50), nullable=False, index=True)  # hiring, funding, partnership, acquisition, etc.
    
    # Signal content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    
    # Source
    source_url = Column(Text, nullable=True)
    source_type = Column(String(50), nullable=True, default="news")  # news, linkedin, manual, twitter, etc.
    source_author = Column(String(255), nullable=True)
    source_published_at = Column(DateTime(timezone=True), nullable=True)
    
    # Related entities
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True, index=True)
    person_id = Column(String(36), ForeignKey("people.id"), nullable=True, index=True)
    
    # Signal metadata
    confidence = Column(Float, default=0.8)  # 0.0 to 1.0
    sentiment = Column(String(20), nullable=True, default="neutral")  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    
    # Categories and tags
    categories = Column(Text, nullable=True)  # JSON array of categories
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # User who created/imported the signal
    # user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="signals")
    person = relationship("Person", back_populates="signals")
    # user = relationship("User", back_populates="signals")
    
    def __repr__(self):
        return f"<Signal(id={self.id}, type={self.signal_type}, title={self.title[:50]})>"


# Import Boolean after class definition
from sqlalchemy import Boolean
