from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from datetime import timedelta
from core.database import get_db
from db.models import Account, Student, Professor
from db.models.account import UserType
from db.schemas.account import (
    AccountCreate, AccountRead, AccountUpdate, AccountLogin, Token
)
from services.auth import (
    get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user, get_current_active_user
)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=AccountRead)
async def register(
    account_data: AccountCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account (student or professor).
    """
    # Check if username or email already exists
    result = await db.execute(
        select(Account).where(
            or_(
                Account.username == account_data.username,
                Account.email == account_data.email
            )
        )
    )
    existing_account = result.scalars().first()
    
    if existing_account:
        if existing_account.username == account_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Check if the specified student or professor exists
    if account_data.user_type == UserType.STUDENT and account_data.student_id:
        student = await db.get(Student, account_data.student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {account_data.student_id} not found"
            )
    
    if account_data.user_type == UserType.PROFESSOR and account_data.professor_id:
        professor = await db.get(Professor, account_data.professor_id)
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Professor with ID {account_data.professor_id} not found"
            )
    
    # Create new account with hashed password
    new_account = Account(
        username=account_data.username,
        email=account_data.email,
        hashed_password=get_password_hash(account_data.password),
        user_type=account_data.user_type,
        student_id=account_data.student_id if account_data.user_type == UserType.STUDENT else None,
        professor_id=account_data.professor_id if account_data.user_type == UserType.PROFESSOR else None
    )
    
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    
    return JSONResponse(content={"data": jsonable_encoder(new_account)})

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate a user and return an access token.
    """
    # Find the user by username
    result = await db.execute(select(Account).where(Account.username == form_data.username))
    user = result.scalars().first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is inactive"
        )
    
    # Create access token with user information
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "user_type": user.user_type,
        },
        expires_delta=access_token_expires,
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=AccountRead)
async def get_current_account_info(
    current_user: Account = Depends(get_current_active_user)
):
    """
    Get the current authenticated user's account information.
    """
    return JSONResponse(content={"data": jsonable_encoder(current_user)})

@router.put("/me", response_model=AccountRead)
async def update_account(
    account_data: AccountUpdate,
    current_user: Account = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the current authenticated user's account information.
    """
    # Update username if provided and not already taken
    if account_data.username and account_data.username != current_user.username:
        result = await db.execute(select(Account).where(Account.username == account_data.username))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = account_data.username
    
    # Update email if provided and not already taken
    if account_data.email and account_data.email != current_user.email:
        result = await db.execute(select(Account).where(Account.email == account_data.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = account_data.email
    
    # Update password if provided
    if account_data.password:
        current_user.hashed_password = get_password_hash(account_data.password)
    
    # Update account status if provided (admin only functionality, could be restricted)
    if account_data.is_active is not None:
        current_user.is_active = account_data.is_active
    
    if account_data.is_verified is not None:
        current_user.is_verified = account_data.is_verified
    
    await db.commit()
    await db.refresh(current_user)
    
    return JSONResponse(content={"data": jsonable_encoder(current_user)})
