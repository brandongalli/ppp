from fastapi import APIRouter, HTTPException, status
from auth.models import User
from auth.schemas import Token
from auth.provider import (
    authenticate_user,
    create_access_token,
    get_user,
    get_password_hash,
)
from db_config import engine

from sqlmodel import Session

router = APIRouter()


@router.post("/token")
async def login_for_access_token(user: User) -> Token:
    user = authenticate_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register_user(user: User):
    current_user = get_user(user.email)
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already exists"
        )
    user.password = get_password_hash(user.password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
