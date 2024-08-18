from fastapi import FastAPI

from src.users.repository.database import engine
from src.users.repository import models
from src.users.users import router as user_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chillzone birthdays API")


app.include_router(user_router)
