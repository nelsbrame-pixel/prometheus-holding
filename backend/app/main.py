from fastapi import FastAPI
from .database import engine, Base
from .models import User

app = FastAPI(title="PROMETHEUS CORE")

@app.get("/health")
def health():
    return {"status": "online"}

Base.metadata.create_all(bind=engine)