"""
Relationship database model
"""

from sqlalchemy import Column, String, Date, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import Optional

from app.db.base import BaseModel


class Relationship(BaseModel):
    """
    Relationship model for connections between people
    """
    
    __tablename__ = "relationships"
    
    # Relationship participants
    from_person_id = Column(String(36), ForeignKey("people.id"), nullable=False, index=True)
    to_person_id = Column(String(36), ForeignKey("people.id"), nullable=False, index=True)
    
    # Relationship type
    relationship_type = Column(String(50), nullable=False, index=True)  # colleague, classmate, family, etc.
    
    # Relationship details
    from_date = Column(Date, nullable=True)
    to_date = Column(Date, nullable=True)
    current = Column(Boolean, default=True)
    
    # Source of the relationship
    source = Column(String(50), nullable=True, default="linkedin")  # linkedin, manual, imported, etc.
    source_url = Column(Text, nullable=True)
    
    # Additional information
    notes = Column(Text, nullable=True)
    strength = Column(Integer, nullable=True)  # 1-10, strength of relationship
    
    # Constraints
    __table_args__ = (
        # Unique constraint: one relationship of each type between two people
        # (A -> B as colleague is different from A -> B as classmate)
        # But we allow bidirectional relationships
        # So we don't add a unique constraint here
        # Instead, we'll handle this in the application logic
        {},
    )
    
    # Relationships
    from_person = relationship("Person", foreign_keys=[from_person_id], back_populates="from_relationships")
    to_person = relationship("Person", foreign_keys=[to_person_id], back_populates="to_relationships")
    
    def __repr__(self):
        return f"<Relationship(id={self.id}, from={self.from_person_id}, to={self.to_person_id}, type={self.relationship_type})>"
