from fastapi import FastAPI

from app.database import create_db_and_tables
from app.models import User


app = FastAPI(
    title="CampusReserve API"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def home():
    return {
        "message": "Welcome to CampusReserve API"
    }