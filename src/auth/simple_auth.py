#!/usr/bin/env python3
"""
Simplified Authentication System without bcrypt dependencies
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel
import hashlib
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple password hashing using SHA256 (for demo purposes only)
def simple_hash_password(password: str) -> str:
    """Simple password hashing for demo - use bcrypt in production"""
    return hashlib.sha256(password.encode()).hexdigest()

# User models
class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Mock user database with simple password hashing
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@securedoc-ai.com",
        "full_name": "System Administrator",
        "hashed_password": simple_hash_password("admin123"),
        "disabled": False,
    },
    "amer": {
        "username": "amer",
        "email": "ajaber1973@web.de",
        "full_name": "Amer Almohammad",
        "hashed_password": simple_hash_password("demo123"),
        "disabled": False,
    },
    "viewer": {
        "username": "viewer",
        "email": "viewer@securedoc-ai.com",
        "full_name": "Document Viewer",
        "hashed_password": simple_hash_password("view123"),
        "disabled": False,
    }
}

class SimpleAuthSystem:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return simple_hash_password(plain_password) == hashed_password
    
    def get_user(self, username: str) -> Optional[UserInDB]:
        """Get user from database"""
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user"""
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[UserInDB]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            token_data = TokenData(username=username)
        except JWTError:
            return None
        user = self.get_user(username=token_data.username)
        return user

# Global auth instance
auth_system = SimpleAuthSystem()

# Test the authentication
if __name__ == "__main__":
    # Test authentication
    user = auth_system.authenticate_user("amer", "demo123")
    if user:
        print(f"✅ Authentication successful for {user.full_name}")
        token = auth_system.create_access_token(data={"sub": user.username})
        print(f"🔑 Token: {token}")
        
        # Verify token
        verified_user = auth_system.verify_token(token)
        if verified_user:
            print(f"✅ Token verified for {verified_user.full_name}")
    else:
        print("❌ Authentication failed")