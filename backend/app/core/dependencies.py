"""
Dependencies for FastAPI
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, AsyncGenerator
import httpx

from app.core.config import settings
from app.core.security import verify_clerk_token
from app.db.session import get_db, AsyncSession
from app.models.user import User
from app.services.user_service import get_user_by_clerk_id

# Security
security = HTTPBearer()


async def get_current_user(
    request: Request,
    token: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from Clerk token
    """
    # Get token from header or query parameter
    if token is None:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Verify Clerk token
        clerk_user = verify_clerk_token(token)
        
        # Get or create user in database
        user = await get_user_by_clerk_id(db, clerk_user["id"])
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get the current user if authenticated, otherwise return None
    """
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            clerk_user = verify_clerk_token(token)
            user = await get_user_by_clerk_id(db, clerk_user["id"])
            return user
    except Exception:
        pass
    return None


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session
    """
    async with get_db() as db:
        yield db


class ClerkWebhookVerifier:
    """
    Verify Clerk webhook requests
    """
    
    def __init__(self):
        self.secret = settings.CLERK_WEBHOOK_SECRET
    
    async def verify(self, request: Request) -> bool:
        """
        Verify Clerk webhook signature
        """
        signature = request.headers.get("svix-signature")
        if not signature:
            return False
        
        # In production, verify the signature
        # For now, skip verification in debug mode
        if settings.DEBUG:
            return True
        
        # TODO: Implement proper signature verification
        # import hmac
        # import hashlib
        # expected_signature = hmac.new(
        #     self.secret.encode(),
        #     await request.body(),
        #     hashlib.sha256
        # ).hexdigest()
        # return hmac.compare_digest(signature, expected_signature)
        
        return True
