import re

from pydantic import BaseModel, validator

from .constants import EMAIL_REGEX


class UserSchema(BaseModel):
    id: int
    name: str
    email: str

class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UpdateUserSchema(BaseModel):
    name: str
    email: str

    @validator('email')
    def domain_to_email(cls, email):
        if not email or re.match(EMAIL_REGEX, email):
            return email

        return f'{email}@fast.com'
