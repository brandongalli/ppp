from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from auth.models import User
from db_config import engine
from settings import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Parameters:
    - plain_password: The password entered by the user.
    - hashed_password: The stored hashed password to verify against.

    Returns:
    - True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Parameters:
    - password: The plain password to be hashed.

    Returns:
    - The hashed password.
    """
    return pwd_context.hash(password)

def get_user(user_email: str) -> User | None:
    """
    Retrieve a user from the database by email.

    Parameters:
    - user_email: The email of the user to be retrieved.

    Returns:
    - The user object if found, None otherwise.
    """
    with Session(engine) as session:
        # Create a select statement to find the user by email
        statement = select(User).where(User.email == user_email)
        results = session.exec(statement)
        user = results.first()
        return user

def authenticate_user(user: User) -> User | bool:
    """
    Authenticate a user by verifying their email and password.

    Parameters:
    - user: A user object containing the email and plain password.

    Returns:
    - The user object if authentication is successful, False otherwise.
    """
    user_from_db = get_user(user.email)
    if not user_from_db:
        # If no user found with that email, return False
        return False
    if not verify_password(user.password, user_from_db.password):
        # If the password does not match, return False
        return False
    return user

def create_access_token(data: dict, expires_minutes: int | None = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Create a JWT access token.

    Parameters:
    - data: The payload data to encode in the token.
    - expires_minutes: Expiration time in minutes (default from settings).

    Returns:
    - The encoded JWT token.
    """
    to_encode = data.copy()
    # Set expiration for the token
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    # Encode the token with JWT_SECRET and ALGORITHM
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt

async def authorization(request: Request) -> bool:
    """
    Authorize a user based on the Authorization header containing a Bearer token.

    Parameters:
    - request: The incoming HTTP request containing headers.

    Returns:
    - True if the token is valid, raises HTTPException otherwise.
    """
    auth_header = request.headers.get("Authorization")

    # Check if the Authorization header exists and starts with "Bearer"
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract the token from the Authorization header
    token = auth_header.split(" ")[1]

    try:
        # Decode the JWT and validate the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        # Fetch user from the database using the email in the token payload
        user: User = get_user(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain a valid username",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        # Raise an HTTPException if token decoding fails
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return True
