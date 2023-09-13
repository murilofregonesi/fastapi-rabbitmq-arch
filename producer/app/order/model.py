from sqlalchemy import Integer, Column, DateTime, ForeignKey, Boolean, String, func
from sqlalchemy.sql import expression

from app.database import Base


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    details = Column(String(512))
    closed = Column(Boolean, server_default=expression.false(), index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)

    def __init__(self, details: str, user_id: int):
        self.details = details
        self.created_by = user_id
