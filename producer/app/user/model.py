from sqlalchemy import Integer, String, Column

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
