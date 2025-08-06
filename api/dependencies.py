from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Generator

from core.security import verify_token
from models.user import User
from database import get_db
from crud.user import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that:
    - Validates the JWT
    - Retrieves the corresponding user from the database
    - Verifies that it is active
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token, credentials_exception)
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = get_user_by_email(db, user_email)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Specific dependency for admin routes.
    Checks that the user has the ‘admin’ role.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user