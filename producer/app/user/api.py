from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import logger
from app.auth.utils import get_current_active_user
from app.database import get_db
from app.rmq_connector import RMQExchangeConnector
from .model import User
from .schema import UserSchema, CreateUserSchema, UpdateUserSchema


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

            routing_key = rmq.create_queue(queue='user.info', binding_key='user.*')
            rmq.basic_publish(routing_key=routing_key, body=f'User {body.email} created.')

        except IntegrityError:
            routing_key = rmq.create_queue(queue='user.error', binding_key='user.error')
            rmq.basic_publish(routing_key=routing_key, body=f'User creation failed to email {body.email}.')

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered',
            )

@user_router.put('/', status_code=status.HTTP_204_NO_CONTENT)
def update_user(
    body: UpdateUserSchema,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Update user data.
    Emails without domain will be automatically filled with '@fast.com'.

    Args:
        body (UpdateUserSchema): Data for user update

    Raises:
        HTTPException: 400
    """
    with RMQExchangeConnector(exchange='producer_log', exchange_type='topic') as rmq:
        try:
            db.query(User).filter(
                User.id == current_user.id
            ).update({
                'name': body.name or current_user.name,
                'email': body.email or current_user.email,
            })
            db.commit()

            routing_key = rmq.create_queue(queue='user.info', binding_key='user.*')
            rmq.basic_publish(routing_key=routing_key, body=f'User {current_user.id} updated.')

        except Exception as error:
            routing_key = rmq.create_queue(queue='user.error', binding_key='user.error')
            rmq.basic_publish(routing_key=routing_key, body=f'User {current_user.id} update has failed.')

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error,
            )
