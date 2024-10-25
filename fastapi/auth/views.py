from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from auth.models import User
from auth.schemas import Token
from auth.provider import (
    authenticate_user,
    create_access_token,
    get_user,
    get_password_hash,
)
from db_config import engine

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(user: User) -> Token:
    """
    Authenticate a user and return an access token.

    Parameters:
    - user: User object containing login credentials (email and password).

    Returns:
    - Token: An access token with a bearer token type if authentication is successful.

    Raises:
    - HTTPException: If authentication fails due to incorrect username or password.
    """
    # Verify the user's credentials
    user = authenticate_user(user)
    if not user:
        # Raise an HTTP exception if credentials are incorrect
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create an access token for the authenticated user
    access_token = create_access_token(data={"sub": user.email})

    # Return the generated access token
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User)
async def register_user(user: User) -> User:
    """
    Register a new user in the system.

    Parameters:
    - user: User object containing user details (email, password, etc.).

    Returns:
    - User: The registered user object.

    Raises:
    - HTTPException: If a user with the same email already exists.
    """
    # Check if the user already exists in the database
    current_user = get_user(user.email)
    if current_user:
        # Raise an HTTP exception if the user already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    # Hash the user's password before saving to the database
    user.password = get_password_hash(user.password)
    with Session(engine) as session:
        # Add the new user to the session and commit changes
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Return the newly created user
        return user
