"""
Company Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.db.models.company import Company as CompanyDB


class CompanyBase(BaseModel):
    """Base company model"""
    name: str = Field(..., description="Company name")
    domain: Optional[str] = Field(None, description="Company domain")
    industry: Optional[str] = Field(None, description="Company industry")
    size: Optional[str] = Field(None, description="Company size")


class CompanyCreate(CompanyBase):
    """Company create model"""
    pass


class CompanyUpdate(BaseModel):
    """Company update model"""
    name: Optional[str] = Field(None, description="Company name")
    domain: Optional[str] = Field(None, description="Company domain")
    industry: Optional[str] = Field(None, description="Company industry")
    size: Optional[str] = Field(None, description="Company size")
    description: Optional[str] = Field(None, description="Company description")
    logo_url: Optional[str] = Field(None, description="Company logo URL")
    website_url: Optional[str] = Field(None, description="Company website URL")
    linkedin_url: Optional[str] = Field(None, description="Company LinkedIn URL")
    twitter_url: Optional[str] = Field(None, description="Company Twitter URL")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    address: Optional[str] = Field(None, description="Address")
    founded_year: Optional[int] = Field(None, description="Founded year")
    last_funding_amount: Optional[int] = Field(None, description="Last funding amount")
    is_public: Optional[bool] = Field(None, description="Is public")
    is_verified: Optional[bool] = Field(None, description="Is verified")


class Company(CompanyBase):
    """Company model with ID"""
    id: str = Field(..., description="Company ID")
    clerk_id: Optional[str] = Field(None, description="Clerk company ID")
    description: Optional[str] = Field(None, description="Company description")
    logo_url: Optional[str] = Field(None, description="Company logo URL")
    website_url: Optional[str] = Field(None, description="Company website URL")
    linkedin_url: Optional[str] = Field(None, description="Company LinkedIn URL")
    twitter_url: Optional[str] = Field(None, description="Company Twitter URL")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    address: Optional[str] = Field(None, description="Address")
    founded_year: Optional[int] = Field(None, description="Founded year")
    last_funding_amount: Optional[int] = Field(None, description="Last funding amount")
    is_public: bool = Field(default=True, description="Is public")
    is_verified: bool = Field(default=False, description="Is verified")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class CompanyResponse(Company):
    """Company response model"""
    pass


class CompanyListResponse(BaseModel):
    """List of companies response"""
    companies: list[CompanyResponse]
    total: int
    page: int
    per_page: int
