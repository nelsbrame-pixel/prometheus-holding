from apscheduler.schedulers.background import BackgroundScheduler

from .database import SessionLocal
from .models.agent import Agent
from .models.agent_log import AgentLog
from .agents.core import run_agent


def run_agents():
    db = SessionLocal()

    agents = db.query(Agent).filter(Agent.active == True).all()

    for agent in agents:
        result = run_agent(agent, db)

        log = AgentLog(
            agent_name=agent.name,
            action=result["action"],
            result=result["result"],
            timestamp=result["time"]
        )

        agent.last_run = result["time"]

        db.add(log)

    db.commit()
    db.close()


def start_worker():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agents, "interval", seconds=60)
    scheduler.start()

    print("[PROMETHEUS] Worker inteligente ativo")