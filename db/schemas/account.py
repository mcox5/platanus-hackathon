from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Union
from datetime import datetime
from enum import Enum

# User type enum
class UserType(str, Enum):
    STUDENT = "student"
    PROFESSOR = "professor"

# Base Account Schema
class AccountBase(BaseModel):
    username: str
    email: EmailStr

# Schema for account creation
class AccountCreate(AccountBase):
    password: str
    user_type: UserType
    student_id: Optional[int] = None
    professor_id: Optional[int] = None
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # Additional password strength checks could be added here
        return v
    
    @validator('student_id', 'professor_id')
    def validate_id_by_type(cls, v, values):
        user_type = values.get('user_type')
        field_name = None
        
        if 'student_id' in values.field_names:
            field_name = 'student_id'
        elif 'professor_id' in values.field_names:
            field_name = 'professor_id'
            
        if user_type == UserType.STUDENT and field_name == 'professor_id' and v is not None:
            raise ValueError('professor_id should be None for student accounts')
        elif user_type == UserType.PROFESSOR and field_name == 'student_id' and v is not None:
            raise ValueError('student_id should be None for professor accounts')
        
        return v

# Schema for reading account data
class AccountRead(AccountBase):
    id: int
    user_type: UserType
    student_id: Optional[int] = None
    professor_id: Optional[int] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Schema for updating account data
class AccountUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    
    @validator('password')
    def password_strength(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    class Config:
        orm_mode = True

# Schema for login
class AccountLogin(BaseModel):
    username: str
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str
    
# Schema for token data (encoded in JWT)
class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    user_type: Optional[str] = None
    exp: Optional[datetime] = None
