from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base
from .models.user import User
from .schemas import UserCreate

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/register")
def register(user: UserCreate):
    return {
        "message": "Usuário recebido com sucesso",
        "email": user.email
    }