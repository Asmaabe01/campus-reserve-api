from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models.user import User
from app.routers import users


app = FastAPI(
    title="CampusReserve API"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CampusReserve API"
    }