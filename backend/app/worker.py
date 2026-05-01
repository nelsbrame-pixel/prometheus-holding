from apscheduler.schedulers.background import BackgroundScheduler
import random

from .database import SessionLocal
from .models.agent import Agent
from .models.agent_log import AgentLog
from .models.task import Task
from .agents.core import run_agent
from .agents.governor import evaluate_agents, enforce_limits


def evaluate_task(task):
    return round(random.uniform(0.3, 1.0), 2)


def process_tasks(db):
    tasks = db.query(Task).filter(Task.status == "pending").all()

    for task in tasks:
        print(f"[TASK] Executando {task.action}")

        task.status = "running"

        if task.action == "incentivar_cadastro":
            task.result = "Campanha executada"

        elif "analisar_total_usuarios" in task.action:
            task.result = "Relatório gerado"

        elif task.action == "priorizar_execucao":
            task.result = "Fila otimizada"

        elif task.action == "monitorar_fila":
            task.result = "Fila monitorada"

        else:
            task.result = "Ação do sistema"

        score = evaluate_task(task)

        log = AgentLog(
            agent_name=task.agent_name,
            action=task.action,
            result=task.result,
            score=score
        )
        db.add(log)

        task.status = "done"

    db.commit()


def run_agents():
    db = SessionLocal()

    try:
        # GOVERNANÇA
        evaluate_agents(db)
        enforce_limits(db)

        agents = db.query(Agent).filter(Agent.active == True).all()

        for agent in agents:
            result = run_agent(agent, db)

            log = AgentLog(
                agent_name=agent.name,
                action=result["action"],
                result=result["result"],
                score=0.0
            )

            db.add(log)

        process_tasks(db)

        db.commit()

    finally:
        db.close()  # 🔥 ESSENCIAL


def start_worker():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        run_agents,
        "interval",
        seconds=30,        # ↑ menos agressivo
        max_instances=1    # 🔥 evita concorrência
    )

    scheduler.start()

    print("[PROMETHEUS] Governança + Pool estabilizado")