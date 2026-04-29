from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .schemas import UserCreate, UserLogin
from .auth import hash_password, verify_password, create_access_token

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)


# DB DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HEALTH
@app.get("/health")
def health():
    return {"status": "online"}


# REGISTER
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

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


# LOGIN (AUTH REAL)
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Senha incorreta")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }