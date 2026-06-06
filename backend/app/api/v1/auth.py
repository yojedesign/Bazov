"""
Authentication endpoints for Clerk integration
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import httpx

from app.core.config import settings
from app.core.dependencies import get_current_user, ClerkWebhookVerifier
from app.core.security import verify_clerk_token
from app.db.session import get_db, AsyncSession
from app.models.user import User, UserCreate, UserUpdate, UserResponse
from app.services.user_service import (
    get_user_by_clerk_id,
    create_user,
    update_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/webhook", response_model=Dict[str, Any])
async def clerk_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Clerk webhook handler for user events
    
    This endpoint receives webhook events from Clerk for:
    - user.created
    - user.updated
    - user.deleted
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        dict: Webhook response
    """
    # Verify webhook signature
    verifier = ClerkWebhookVerifier()
    if not await verifier.verify(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )
    
    # Parse webhook data
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON: {str(e)}",
        )
    
    event_type = data.get("type")
    event_data = data.get("data", {})
    
    # Handle different event types
    if event_type == "user.created":
        await _handle_user_created(db, event_data)
    elif event_type == "user.updated":
        await _handle_user_updated(db, event_data)
    elif event_type == "user.deleted":
        await _handle_user_deleted(db, event_data)
    else:
        # Ignore unknown event types
        pass
    
    return {"status": "ok", "event": event_type}


async def _handle_user_created(db: AsyncSession, user_data: Dict[str, Any]):
    """Handle user.created webhook event"""
    clerk_id = user_data.get("id")
    email = user_data.get("email_addresses", [{}])[0].get("email_address")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    username = user_data.get("username")
    avatar_url = user_data.get("image_url")
    
    # Check if user already exists
    existing_user = await get_user_by_clerk_id(db, clerk_id)
    if existing_user:
        # User already exists, update if needed
        update_data = UserUpdate(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            avatar_url=avatar_url,
        )
        await update_user(db, existing_user.id, update_data)
        return
    
    # Create new user
    user_create = UserCreate(
        clerk_id=clerk_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
        username=username,
        avatar_url=avatar_url,
    )
    await create_user(db, user_create)


async def _handle_user_updated(db: AsyncSession, user_data: Dict[str, Any]):
    """Handle user.updated webhook event"""
    clerk_id = user_data.get("id")
    email = user_data.get("email_addresses", [{}])[0].get("email_address")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    username = user_data.get("username")
    avatar_url = user_data.get("image_url")
    
    # Find and update user
    user = await get_user_by_clerk_id(db, clerk_id)
    if user:
        update_data = UserUpdate(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            avatar_url=avatar_url,
        )
        await update_user(db, user.id, update_data)


async def _handle_user_deleted(db: AsyncSession, user_data: Dict[str, Any]):
    """Handle user.deleted webhook event"""
    clerk_id = user_data.get("id")
    
    # Find and deactivate user (soft delete)
    user = await get_user_by_clerk_id(db, clerk_id)
    if user:
        update_data = UserUpdate(is_active=False)
        await update_user(db, user.id, update_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Get the current authenticated user
    
    Args:
        current_user: The authenticated user from dependencies
        
    Returns:
        UserResponse: The current user's information
    """
    return UserResponse.from_orm(current_user)


@router.post("/token", response_model=Dict[str, Any])
async def verify_token(
    token: str = Body(..., embed=True),
) -> Dict[str, Any]:
    """
    Verify a Clerk JWT token
    
    Args:
        token: The Clerk JWT token to verify
        
    Returns:
        dict: The decoded token payload
    """
    try:
        user_data = await verify_clerk_token(token)
        return {
            "valid": True,
            "user": user_data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )


@router.get("/clerk-config", response_model=Dict[str, Any])
async def get_clerk_config() -> Dict[str, Any]:
    """
    Get Clerk configuration for frontend
    
    Returns:
        dict: Clerk configuration
    """
    return {
        "publishable_key": settings.CLERK_PUBLISHABLE_KEY or "",
        "sign_in_url": "https://bazov.clerk.accounts.dev/sign-in",
        "sign_up_url": "https://bazov.clerk.accounts.dev/sign-up",
        "user_profile_url": "https://bazov.clerk.accounts.dev/user",
    }
