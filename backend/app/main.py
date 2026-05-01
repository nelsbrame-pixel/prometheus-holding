from .models.agent import Agent

@app.post("/agents")
def create_agent(name: str, db: Session = Depends(get_db)):
    agent = Agent(name=name)

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {"message": "Agente criado", "id": agent.id}