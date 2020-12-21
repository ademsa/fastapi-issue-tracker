import typing
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from fastapi_issue_tracker.config import settings
from fastapi_issue_tracker.data import crud, models
from fastapi_issue_tracker.data.database import Database

AUTH_OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth")
AUTH_CRYPT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_user_credentials(
    username: str, password: str, db: Session = Depends(Database.get_db)
) -> typing.Optional[models.User]:
    user = crud.get_user_by_username(db, username)

    if not user or not AUTH_CRYPT_CONTEXT.verify(password, user.password):
        return None

    return user


def generate_token(username: str) -> typing.Any:
    claims = {
        "sub": username,
        "exp": datetime.utcnow()
        + timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_IN_MIN),
    }
    return jwt.encode(
        claims, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM
    )


def get_current_user(
    token: str = Depends(AUTH_OAUTH2_SCHEME), db: Session = Depends(Database.get_db)
) -> models.User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not authenticate.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        claims = jwt.decode(
            token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM]
        )
        username = claims.get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    user = crud.get_user_by_username(db, username)

    if user is None:
        raise exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
