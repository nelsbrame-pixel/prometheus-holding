from fastapi import FastAPI
from app.database import engine, Base
from app.models import User

app = FastAPI(title="PROMETHEUS CORE")

@app.get("/health")
def health():
    return {"status": "online"}

Base.metadata.create_all(bind=engine)