from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .utils import authenticate_user, create_access_token
from .schema import Token
from .constant import ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter(
    tags=['Auth']
)

@auth_router.post('/token', response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate and create an access token for an user.

    Args:
        body (UserLoginSchema): Login data

    Raises:
        HTTPException: 401

    Returns:
        dict: access token data
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
