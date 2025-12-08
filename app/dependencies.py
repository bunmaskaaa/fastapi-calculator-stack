from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from .database import get_db
from . import models
from .core.security import SECRET_KEY, ALGORITHM

# This is only used for OpenAPI docs; it won't affect runtime token validation.
# Adjust the tokenUrl if your login endpoint is different (e.g. "/api/auth/login").
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Dependency that:
    - extracts the JWT token from the Authorization header
    - decodes it
    - fetches the user from the database
    - raises 401 if anything is invalid
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token using the same SECRET_KEY and ALGORITHM that
        # create_access_token in core.security uses.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        if sub is None:
            raise credentials_exception

        # We assume "sub" contains the user ID as a string.
        # If your create_access_token uses email instead, we can adjust later.
        user_id = int(sub)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user