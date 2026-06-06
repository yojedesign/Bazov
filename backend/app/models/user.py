"""
User Pydantic models
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

from app.db.models.user import User as UserDB


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr = Field(..., description="User email address")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    username: Optional[str] = Field(None, description="User username")
    avatar_url: Optional[str] = Field(None, description="URL to user avatar")


class UserCreate(UserBase):
    """User creation model"""
    clerk_id: str = Field(..., description="Clerk user ID")


class UserUpdate(BaseModel):
    """User update model"""
    email: Optional[EmailStr] = Field(None, description="User email address")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    username: Optional[str] = Field(None, description="User username")
    avatar_url: Optional[str] = Field(None, description="URL to user avatar")
    theme: Optional[str] = Field(None, description="UI theme preference")
    language: Optional[str] = Field(None, description="Language preference")
    timezone: Optional[str] = Field(None, description="Timezone")
    is_active: Optional[bool] = Field(None, description="Is user active")
    is_verified: Optional[bool] = Field(None, description="Is user verified")


class User(UserBase):
    """User model with ID"""
    id: str = Field(..., description="User ID")
    clerk_id: str = Field(..., description="Clerk user ID")
    theme: str = Field(default="system", description="UI theme preference")
    language: str = Field(default="en", description="Language preference")
    timezone: str = Field(default="UTC", description="Timezone")
    is_active: bool = Field(default=True, description="Is user active")
    is_verified: bool = Field(default=False, description="Is user verified")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        from_attributes = True


class UserResponse(User):
    """User response model"""
    pass


class UserListResponse(BaseModel):
    """User list response model"""
    items: list[UserResponse] = Field(default_factory=list, description="List of users")
    total: int = Field(default=0, description="Total number of users")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=10, description="Items per page")
    pages: int = Field(default=0, description="Total number of pages")
