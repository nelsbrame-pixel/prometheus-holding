from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .schemas import UserCreate, UserLogin, Token
from .auth import hash_password, verify_password, create_access_token
from .worker import start_worker

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)

# 🔥 inicia o cérebro automático
start_worker()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "online"}