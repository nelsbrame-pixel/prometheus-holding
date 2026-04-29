from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .schemas import UserCreate

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        hashed_password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Usuário salvo com sucesso",
        "id": new_user.id,
        "email": new_user.email
    }