"""
User service for business logic
"""

from typing import Optional, List
from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User as UserDB
from app.models.user import UserCreate, UserUpdate, UserResponse


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[UserDB]:
    """
    Get a user by ID
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        UserDB or None
    """
    result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_clerk_id(db: AsyncSession, clerk_id: str) -> Optional[UserDB]:
    """
    Get a user by Clerk ID
    
    Args:
        db: Database session
        clerk_id: Clerk user ID
        
    Returns:
        UserDB or None
    """
    result = await db.execute(
        select(UserDB).where(UserDB.clerk_id == clerk_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[UserDB]:
    """
    Get a user by email
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        UserDB or None
    """
    result = await db.execute(
        select(UserDB).where(UserDB.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserDB:
    """
    Create a new user
    
    Args:
        db: Database session
        user_data: User creation data
        
    Returns:
        UserDB: Created user
    """
    user_dict = user_data.model_dump()
    user = UserDB(**user_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    db: AsyncSession,
    user_id: str,
    user_data: UserUpdate,
) -> Optional[UserDB]:
    """
    Update a user
    
    Args:
        db: Database session
        user_id: User ID
        user_data: User update data
        
    Returns:
        UserDB or None
    """
    update_data = user_data.model_dump(exclude_unset=True)
    
    if not update_data:
        return None
    
    result = await db.execute(
        sql_update(UserDB)
        .where(UserDB.id == user_id)
        .values(**update_data)
        .returning(UserDB)
    )
    user = result.scalar_one_or_none()
    await db.commit()
    return user


async def delete_user(db: AsyncSession, user_id: str) -> bool:
    """
    Delete a user (soft delete)
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    result = await db.execute(
        sql_update(UserDB)
        .where(UserDB.id == user_id)
        .values(is_active=False)
    )
    await db.commit()
    return result.rowcount > 0


async def list_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
) -> tuple[List[UserDB], int]:
    """
    List users with pagination
    
    Args:
        db: Database session
        skip: Number of items to skip
        limit: Maximum number of items to return
        search: Optional search term
        
    Returns:
        tuple: (list of users, total count)
    """
    query = select(UserDB).where(UserDB.is_active == True)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            UserDB.email.ilike(search_pattern) |
            UserDB.first_name.ilike(search_pattern) |
            UserDB.last_name.ilike(search_pattern) |
            UserDB.username.ilike(search_pattern)
        )
    
    # Get total count
    count_result = await db.execute(
        select([func.count()]).select_from(query.subquery())
    )
    total = count_result.scalar() or 0
    
    # Get paginated results
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users, total
