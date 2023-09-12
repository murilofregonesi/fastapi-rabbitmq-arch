from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.user.api import user_router
from app.order.api import order_router
from app.database import Base, engine

# import all model files for database recognition
from app.user import model
from app.order import model


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(order_router)
