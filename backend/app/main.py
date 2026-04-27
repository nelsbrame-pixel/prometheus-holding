from fastapi import FastAPI

app = FastAPI(title="PROMETHEUS CORE")

@app.get("/health")
def health():
    return {"status": "online"}