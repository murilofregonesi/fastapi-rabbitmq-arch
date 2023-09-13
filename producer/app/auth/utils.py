from datetime import timedelta, datetime
from typing import Annotated

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal
from app.user.model import User
from .constant import SECRET_KEY, ALGORITHM
from .schema import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user or not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(email: str) -> User:
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
    finally:
        db.close()
    return user


def get_current_active_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    current_user = get_user(email=token_data.email)
    if current_user is None:
        raise credentials_exception

    return current_user
