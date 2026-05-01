from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from .models.user import User
from .models.agent import Agent
from .models.task import Task
from .schemas import UserCreate, UserLogin
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

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
    hashed = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password=hashed,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário criado"}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = create_access_token({"sub": db_user.email})

    return {"access_token": token}


@app.post("/agents")
def create_agent(
    name: str,
    type: str = "generic",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    agent = Agent(name=name, type=type)

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": f"Agente criado por {current_user.email}",
        "id": agent.id,
        "type": agent.type
    }


@app.get("/tasks")
def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")

    return db.query(Task).all()