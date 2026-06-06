"""
Person database model
"""

from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import BaseModel


class Person(BaseModel):
    """
    Person model for individuals (from LinkedIn, manual entry, etc.)
    """
    
    __tablename__ = "people"
    
    # External IDs
    linkedin_id = Column(String(255), nullable=True, unique=True, index=True)
    twitter_id = Column(String(255), nullable=True, unique=True)
    github_id = Column(String(255), nullable=True, unique=True)
    
    # Personal information
    first_name = Column(String(255), nullable=False, index=True)
    last_name = Column(String(255), nullable=False, index=True)
    full_name = Column(String(510), nullable=True, index=True)
    
    # Current position
    current_title = Column(String(255), nullable=True)
    current_company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    
    # Bio and summary
    bio = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    
    # Profile URLs
    profile_url = Column(Text, nullable=True)
    avatar_url = Column(Text, nullable=True)
    linkedin_url = Column(Text, nullable=True)
    twitter_url = Column(Text, nullable=True)
    github_url = Column(Text, nullable=True)
    personal_website = Column(Text, nullable=True)
    
    # Contact information
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    
    # Location
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    
    # Education
    education = Column(Text, nullable=True)  # JSON array of education entries
    
    # Skills
    skills = Column(Text, nullable=True)  # JSON array of skills
    
    # Experience
    experience = Column(Text, nullable=True)  # JSON array of work experience
    
    # Status
    is_public = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_updated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    current_company = relationship("Company", foreign_keys=[current_company_id])
    company_roles = relationship("CompanyPerson", back_populates="person")
    from_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.from_person_id",
        back_populates="from_person",
        cascade="all, delete-orphan"
    )
    to_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.to_person_id",
        back_populates="to_person",
        cascade="all, delete-orphan"
    )
    signals = relationship("Signal", back_populates="person")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name={self.full_name or f'{self.first_name} {self.last_name}'})>"


# Import Boolean after class definition
from sqlalchemy import Boolean
