"""
Security utilities for authentication and authorization
"""

import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import jwt
from jose import JWTError, jwt as jose_jwt

from app.core.config import settings


async def verify_clerk_token(token: str) -> Dict[str, Any]:
    """
    Verify a Clerk JWT token and return the decoded payload
    
    Args:
        token: The JWT token to verify
        
    Returns:
        The decoded token payload
        
    Raises:
        HTTPException: If the token is invalid
    """
    # Clerk token verification
    # In production, use the Clerk API to verify the token
    
    if settings.DEBUG:
        # In debug mode, return a mock user
        try:
            payload = jose_jwt.decode(
                token,
                settings.CLERK_SECRET_KEY,
                algorithms=["HS256"],
                options={"verify_signature": False}
            )
            return payload
        except JWTError:
            # Return a mock user for development
            return {
                "id": "user_mock_id",
                "email": "mock@example.com",
                "first_name": "Mock",
                "last_name": "User",
            }
    
    # Production: Verify with Clerk API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.clerk.com/v1/users/me",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )
            
            if response.status_code != 200:
                raise ValueError(f"Clerk API error: {response.status_code}")
            
            return response.json()
            
    except Exception as e:
        raise ValueError(f"Failed to verify Clerk token: {str(e)}")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })
    
    encoded_jwt = jose_jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT access token
    
    Args:
        token: The JWT token to decode
        
    Returns:
        The decoded token payload
        
    Raises:
        JWTError: If the token is invalid
    """
    payload = jose_jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )
    
    return payload


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password
    
    Args:
        plain_password: The plain text password
        hashed_password: The hashed password
        
    Returns:
        True if the password matches, False otherwise
    """
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    
    Args:
        password: The password to hash
        
    Returns:
        The hashed password
    """
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    return pwd_context.hash(password)
