from fastapi import FastAPI
from .database import engine, Base
from .models.user import User

app = FastAPI(title="PROMETHEUS CORE")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "online"}