from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from .database import SessionLocal
from .models.agent import Agent
from .agents.core import run_agent


def run_agents():
    db = SessionLocal()

    agents = db.query(Agent).filter(Agent.active == True).all()

    for agent in agents:
        result = run_agent(agent)

        agent.last_run = result["time"]

    db.commit()
    db.close()


def start_worker():
    scheduler = BackgroundScheduler()

    scheduler.add_job(run_agents, "interval", seconds=60)

    scheduler.start()

    print("[PROMETHEUS] Worker com agentes iniciado")