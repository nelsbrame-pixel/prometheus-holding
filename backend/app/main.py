from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .database import engine, Base, SessionLocal
from .models.user import User
from .schemas import UserCreate

app = FastAPI(title="PROMETHEUS CORE")

# cria tabelas (ok para início, depois migramos para Alembic)
Base.metadata.create_all(bind=engine)

# hash de senha (SEGURANÇA BÁSICA)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password)


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # verifica se usuário já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"error": "Usuário já existe"}

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Usuário criado com sucesso",
        "id": new_user.id,
        "email": new_user.email
    }