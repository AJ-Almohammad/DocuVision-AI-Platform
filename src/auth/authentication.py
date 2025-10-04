#!/usr/bin/env python3
"""
Authentication and User Management System
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# Mock user database (replace with real database in production)
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@securedoc-ai.com",
        "full_name": "System Administrator",
        "hashed_password": pwd_context.hash("admin123"),
        "disabled": False,
    },
    "amer": {
        "username": "amer",
        "email": "ajaber1973@web.de",
        "full_name": "Amer Almohammad",
        "hashed_password": pwd_context.hash("demo123"),
        "disabled": False,
    }
}

class AuthSystem:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES  # Fixed missing attribute
    
    def verify_password(self, plain_password, hashed_password):
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        """Hash a password"""
        return pwd_context.hash(password)
    
    def get_user(self, username: str):
        """Get user from database"""
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)
        return None
    
    def authenticate_user(self, username: str, password: str):
        """Authenticate a user"""
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str):
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
auth_system = AuthSystem()