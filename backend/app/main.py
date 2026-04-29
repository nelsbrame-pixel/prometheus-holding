from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .schemas import UserCreate

app = FastAPI(title="PROMETHEUS CORE")


# cria tabelas automaticamente (ok para MVP)
Base.metadata.create_all(bind=engine)


# dependência de banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# health check (Render usa isso para saber que está vivo)
@app.get("/health")
def health():
    return {"status": "online"}


# registro de usuário
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        email=user.email,
        hashed_password=user.password  # depois vamos criptografar isso
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Usuário criado com sucesso",
        "id": new_user.id,
        "email": new_user.email
    }