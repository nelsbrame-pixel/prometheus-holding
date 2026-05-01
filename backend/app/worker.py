from apscheduler.schedulers.background import BackgroundScheduler

from .database import SessionLocal
from .models.agent import Agent
from .models.agent_log import AgentLog
from .models.task import Task
from .agents.core import run_agent


def process_tasks(db):
    tasks = db.query(Task).filter(Task.status == "pending").all()

    for task in tasks:
        print(f"[TASK] Executando {task.action}")

        task.status = "running"

        if task.action == "incentivar_cadastro":
            task.result = "Campanha planejada"
        else:
            task.result = "Ação desconhecida"

        task.status = "done"

    db.commit()


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

        db.add(log)

    process_tasks(db)

    db.commit()
    db.close()


def start_worker():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agents, "interval", seconds=60)
    scheduler.start()

    print("[PROMETHEUS] Worker ativo")