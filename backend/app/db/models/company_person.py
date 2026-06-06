"""
Company-Person relationship database model
"""

from sqlalchemy import Column, String, Date, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from typing import Optional

from app.db.base import BaseModel


class CompanyPerson(BaseModel):
    """
    Many-to-many relationship between companies and people
    Represents a person's role at a company
    """
    
    __tablename__ = "company_people"
    
    # Foreign keys
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, index=True)
    person_id = Column(String(36), ForeignKey("people.id"), nullable=False, index=True)
    
    # Role information
    role = Column(String(255), nullable=False)  # e.g., "CEO", "Software Engineer", "Board Member"
    department = Column(String(255), nullable=True)  # e.g., "Engineering", "Sales", "Marketing"
    
    # Employment dates
    started_at = Column(Date, nullable=True)
    ended_at = Column(Date, nullable=True)
    is_current = Column(Boolean, default=True)
    
    # Additional information
    is_board_member = Column(Boolean, default=False)
    is_executive = Column(Boolean, default=False)
    is_founder = Column(Boolean, default=False)
    
    # Source
    source = Column(String(50), nullable=True, default="linkedin")  # linkedin, manual, imported, etc.
    source_url = Column(Text, nullable=True)
    
    # Constraints
    __table_args__ = (
        # Unique constraint: one role per person per company per start date
        # This allows tracking historical roles
        {
            "unique_together": [("company_id", "person_id", "role", "started_at")]
        },
    )
    
    # Relationships
    company = relationship("Company", back_populates="people")
    person = relationship("Person", back_populates="company_roles")
    
    def __repr__(self):
        return f"<CompanyPerson(id={self.id}, company={self.company_id}, person={self.person_id}, role={self.role})>"


# Import Boolean after class definition
from sqlalchemy import Boolean
