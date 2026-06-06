"""
Company database model
"""

from sqlalchemy import Column, String, Text, Integer, Date, DateTime, func
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import BaseModel


class Company(BaseModel):
    """
    Company model for organizations
    """
    
    __tablename__ = "companies"
    
    # Company information
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=True, unique=True, index=True)
    industry = Column(String(255), nullable=True, index=True)
    size = Column(String(50), nullable=True)  # e.g., "1-10", "11-50", "51-200"
    founded_year = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    website_url = Column(Text, nullable=True)
    linkedin_url = Column(Text, nullable=True)
    twitter_url = Column(Text, nullable=True)
    
    # Location
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    
    # Financial
    revenue_range = Column(String(50), nullable=True)
    funding_stage = Column(String(50), nullable=True)  # seed, series_a, series_b, etc.
    last_funding_date = Column(Date, nullable=True)
    last_funding_amount = Column(Integer, nullable=True)  # in USD
    
    # Status
    is_public = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    people = relationship("CompanyPerson", back_populates="company")
    signals = relationship("Signal", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, domain={self.domain})>"


# Import Boolean after class definition
from sqlalchemy import Boolean
