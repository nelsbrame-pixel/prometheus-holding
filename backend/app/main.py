from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .models.agent import Agent
from .schemas import UserCreate

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)


# 🔌 conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ❤️ health check
@app.get("/health")
def health():
    return {"status": "online"}


# 👤 registro de usuário
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


# 🤖 criar agente
@app.post("/agents")
def create_agent(name: str, type: str = "generic", db: Session = Depends(get_db)):
    agent = Agent(name=name, type=type)

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": "Agente criado",
        "id": agent.id,
        "type": agent.type
    }