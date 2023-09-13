from sqlalchemy import Integer, String, Column
from passlib.context import CryptContext

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = self.password_hash(password)

    def verify_password(self, password: str):
        return self.pwd_context.verify(password, self.password)

    def password_hash(self, password: str):
        return self.pwd_context.hash(password)
