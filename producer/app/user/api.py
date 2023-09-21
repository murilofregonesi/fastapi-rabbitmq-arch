from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .model import User
from .schema import UserSchema, CreateUserSchema
from app.database import get_db
from app import logger
from app.rmq_connector import RMQExchangeConnector


user_router = APIRouter(
    prefix='/user',
    tags=['User'],
)

@user_router.get('/list', response_model=List[UserSchema])
def list_users(db: Annotated[Session, Depends(get_db)]) -> List[UserSchema]:
    """List all registered users.

    Returns:
        List[User]: List of all users
    """
    users = db.query(User).all()
    return users

@user_router.get('/{user_id}', response_model=UserSchema)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]) -> UserSchema:
    """Return user by its id.

    Args:
        user_id (int): User id

    Raises:
        HTTPException: 404

    Returns:
        User: User instance
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    return user

@user_router.post('/', status_code=status.HTTP_204_NO_CONTENT)
def create_user(body: CreateUserSchema, db: Annotated[Session, Depends(get_db)]) -> None:
    """Create a new user.

    Args:
        body (CreateUserSchema): User data

    Raises:
        HTTPException: 400
    """
    user = User(
        name=body.name,
        email=body.email,
        password=body.password,
    )
    logger.info(f'New user created: {body.email}')

    with RMQExchangeConnector(exchange='producer_log', exchange_type='topic') as rmq:
        db.add(user)
        try:
            db.commit()

            routing_key = rmq.create_queue('user.info')
            rmq.basic_publish(routing_key=routing_key, body=f'User {body.email} created.')
        except IntegrityError:
            routing_key = rmq.create_queue('user.error')
            rmq.basic_publish(routing_key=routing_key, body=f'User creation failed to email {body.email}.')

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered',
            )
