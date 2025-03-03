from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from security import hash_password, verify_password
from credential import create_access_token
from pydantic import BaseModel

router = APIRouter()

class UserCredential(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user: UserCredential, db: AsyncSession = Depends(get_db)):
    """Registers a new user with hashed password."""

    # Check if user exists using ORM query
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()  # Fetch the first result or None

    print(existing_user)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, name=user.name, password_hash=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserCredential, db: AsyncSession = Depends(get_db)):
    """Logs in a user and returns JWT token."""
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    print(existing_user)

    if not existing_user or not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    jwt_token = create_access_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}
