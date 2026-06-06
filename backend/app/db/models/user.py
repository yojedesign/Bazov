"""
User database model
"""

from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from typing import List, Optional

from app.db.base import BaseModel


class User(BaseModel):
    """
    User model for authenticated users (via Clerk)
    """
    
    __tablename__ = "users"
    
    # Clerk ID
    clerk_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # User information
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True, unique=True)
    avatar_url = Column(Text, nullable=True)
    
    # Preferences
    theme = Column(String(20), default="system")  # light, dark, system
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # signals = relationship("Signal", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, clerk_id={self.clerk_id})>"


# Import Boolean after class definition to avoid circular imports
from sqlalchemy import Boolean
