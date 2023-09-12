from datetime import datetime

from pydantic import BaseModel


class OrderSchema(BaseModel):
    details: str
    closed: bool
    created_at: datetime

class CreateOrderSchema(BaseModel):
    details: str
