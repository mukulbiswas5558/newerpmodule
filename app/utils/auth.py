from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from fastapi import HTTPException,Header
# Configuration for JWT
SECRET_KEY = "your_secret_key"  # Replace with a secure key.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the plain password against the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(token: str):
    """
    Validate the Bearer token and decode its contents.

    Args:
        token (str): Bearer token.

    Returns:
        dict: Decoded payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    
async def get_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and validate the Bearer token from the Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format.")
    return authorization[len("Bearer "):]