"""
Relationship Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.db.models.relationship import Relationship as RelationshipDB


class RelationshipBase(BaseModel):
    """Base relationship model"""
    person1_id: str = Field(..., description="First person ID")
    person2_id: str = Field(..., description="Second person ID")
    relationship_type: str = Field(..., description="Relationship type")


class RelationshipCreate(RelationshipBase):
    """Relationship create model"""
    pass


class RelationshipUpdate(BaseModel):
    """Relationship update model"""
    relationship_type: Optional[str] = Field(None, description="Relationship type")
    strength: Optional[int] = Field(None, description="Relationship strength")
    current: Optional[bool] = Field(None, description="Is current")
    notes: Optional[str] = Field(None, description="Notes")


class Relationship(RelationshipBase):
    """Relationship model with ID"""
    id: str = Field(..., description="Relationship ID")
    strength: int = Field(default=5, ge=1, le=10, description="Relationship strength")
    current: bool = Field(default=True, description="Is current")
    notes: Optional[str] = Field(None, description="Notes")
    source: Optional[str] = Field(None, description="Source")
    source_url: Optional[str] = Field(None, description="Source URL")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class RelationshipResponse(Relationship):
    """Relationship response model"""
    pass


class RelationshipListResponse(BaseModel):
    """List of relationships response"""
    relationships: list[RelationshipResponse]
    total: int
    page: int
    per_page: int


class RelationshipGraphRequest(BaseModel):
    """Request for relationship graph"""
    person_id: str = Field(..., description="Person ID")
    depth: int = Field(default=2, ge=1, le=5, description="Graph depth")


class RelationshipPathRequest(BaseModel):
    """Request for relationship path"""
    person1_id: str = Field(..., description="First person ID")
    person2_id: str = Field(..., description="Second person ID")
    max_depth: int = Field(default=5, ge=1, le=10, description="Maximum path depth")


class RelationshipPathResponse(BaseModel):
    """Response for relationship path"""
    path: list[dict]
    distance: int
