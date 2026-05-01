from apscheduler.schedulers.background import BackgroundScheduler
import random

from .database import SessionLocal
from .models.agent import Agent
from .models.agent_log import AgentLog
from .models.task import Task
from .agents.core import run_agent


def evaluate_task(task):
    # Simulação de desempenho (0 a 1)
    return round(random.uniform(0.3, 1.0), 2)


def process_tasks(db):
    tasks = db.query(Task).filter(Task.status == "pending").all()

    for task in tasks:
        print(f"[TASK] Executando {task.action}")

        task.status = "running"

        # RESULTADO
        if task.action == "incentivar_cadastro":
            task.result = "Campanha executada"

        elif "analisar_total_usuarios" in task.action:
            task.result = "Relatório gerado"

        elif task.action == "priorizar_execucao":
            task.result = "Fila otimizada"

        elif task.action == "monitorar_fila":
            task.result = "Fila monitorada"

        else:
            task.result = "Ação desconhecida"

        # AVALIAÇÃO (AUTO-APRENDIZADO)
        score = evaluate_task(task)

        # REGISTRO COM SCORE
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

    agents = db.query(Agent).all()

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
    db.close()


def start_worker():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agents, "interval", seconds=20)
    scheduler.start()

    print("[PROMETHEUS] Auto-otimização ativa")