from pydantic import BaseModel


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
