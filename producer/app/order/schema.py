from datetime import datetime

from pydantic import BaseModel


class OrderSchema(BaseModel):
    details: str
    closed: bool
    created_at: datetime
    created_by: int

class CreateOrderSchema(BaseModel):
    details: str
