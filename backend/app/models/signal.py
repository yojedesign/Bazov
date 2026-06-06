"""
Signal Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.db.models.signal import Signal as SignalDB


class SignalBase(BaseModel):
    """Base signal model"""
    title: str = Field(..., description="Signal title")
    content: str = Field(..., description="Signal content")


class SignalCreate(SignalBase):
    """Signal create model"""
    pass


class SignalUpdate(BaseModel):
    """Signal update model"""
    title: Optional[str] = Field(None, description="Signal title")
    content: Optional[str] = Field(None, description="Signal content")
    signal_type: Optional[str] = Field(None, description="Signal type")
    summary: Optional[str] = Field(None, description="Signal summary")


class Signal(SignalBase):
    """Signal model with ID"""
    id: str = Field(..., description="Signal ID")
    user_id: Optional[str] = Field(None, description="User ID who created the signal")
    signal_type: str = Field(default="news", description="Signal type")
    summary: Optional[str] = Field(None, description="Signal summary")
    source: Optional[str] = Field(None, description="Signal source")
    source_url: Optional[str] = Field(None, description="Source URL")
    categories: Optional[str] = Field(None, description="Categories")
    tags: Optional[str] = Field(None, description="Tags")
    sentiment: Optional[str] = Field(None, description="Sentiment")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score")
    is_processed: bool = Field(default=False, description="Is processed")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class SignalResponse(Signal):
    """Signal response model"""
    pass


class SignalListResponse(BaseModel):
    """List of signals response"""
    signals: list[SignalResponse]
    total: int
    page: int
    per_page: int


class SignalTypeResponse(BaseModel):
    """Signal type response"""
    types: list[str]
