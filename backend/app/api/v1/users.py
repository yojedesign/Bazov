"""
User endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.core.dependencies import get_current_user, get_db, AsyncSession
from app.db.models.user import User as UserDB
from app.models.user import (
    User,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services.user_service import (
    get_user_by_id,
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
    list_users,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserDB = Depends(get_current_user),
) -> UserResponse:
    """
    Get current user information
    """
    return UserResponse.from_orm(current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[UserDB] = Depends(get_current_user),
) -> UserResponse:
    """
    Get a user by ID
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.from_orm(user)


@router.get("/", response_model=UserListResponse)
async def list_all_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> UserListResponse:
    """
    List all users with pagination
    """
    users, total = await list_users(db, skip=skip, limit=limit, search=search)
    
    pages = (total + limit - 1) // limit if total > 0 else 0
    
    return UserListResponse(
        items=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        pages=pages,
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> UserResponse:
    """
    Create a new user
    """
    # Check if user already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    
    user = await create_user(db, user_data)
    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_existing_user(
    user_id: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> UserResponse:
    """
    Update a user
    """
    # Check if user exists
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if user can update this user
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )
    
    user = await update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update",
        )
    
    return UserResponse.from_orm(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> None:
    """
    Delete a user
    """
    # Check if user exists
    existing_user = await get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if user can delete this user
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )
    
    await delete_user(db, user_id)
