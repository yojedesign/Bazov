"""
Person Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.db.models.person import Person as PersonDB


class PersonBase(BaseModel):
    """Base person model"""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")


class PersonCreate(PersonBase):
    """Person create model"""
    email: Optional[str] = Field(None, description="Email address")
    username: Optional[str] = Field(None, description="Username")


class PersonUpdate(BaseModel):
    """Person update model"""
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    username: Optional[str] = Field(None, description="Username")


class Person(PersonBase):
    """Person model with ID"""
    id: str = Field(..., description="Person ID")
    clerk_id: Optional[str] = Field(None, description="Clerk person ID")
    email: Optional[str] = Field(None, description="Email address")
    username: Optional[str] = Field(None, description="Username")
    bio: Optional[str] = Field(None, description="Biography")
    summary: Optional[str] = Field(None, description="Summary")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    profile_url: Optional[str] = Field(None, description="Profile URL")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    twitter_url: Optional[str] = Field(None, description="Twitter URL")
    github_url: Optional[str] = Field(None, description="GitHub URL")
    personal_website: Optional[str] = Field(None, description="Personal website")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    current_company: Optional[str] = Field(None, description="Current company")
    current_title: Optional[str] = Field(None, description="Current title")
    education: Optional[str] = Field(None, description="Education")
    skills: Optional[str] = Field(None, description="Skills")
    experience: Optional[str] = Field(None, description="Experience")
    is_public: bool = Field(default=True, description="Is public")
    is_verified: bool = Field(default=False, description="Is verified")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        from_attributes = True


class PersonResponse(Person):
    """Person response model"""
    pass


class PersonListResponse(BaseModel):
    """List of persons response"""
    persons: list[PersonResponse]
    total: int
    page: int
    per_page: int
