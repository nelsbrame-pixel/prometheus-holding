from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.user import User
from ..models.task import Task
from ..models.agent import Agent
from ..models.agent_log import AgentLog


MAX_AGENTS = 10
MAX_GENERATION = 3


def get_best_score(db, agent_name):
    result = db.query(func.avg(AgentLog.score)).filter(
        AgentLog.agent_name == agent_name
    ).scalar()

    return result or 0


def can_spawn(db, agent):
    total_agents = db.query(Agent).count()

    if total_agents >= MAX_AGENTS:
        return False

    if agent.generation >= MAX_GENERATION:
        return False

    score = get_best_score(db, agent.name)

    return score > 0.7  # só agentes bons se replicam


def spawn_agent(db, parent_agent):
    new_name = f"{parent_agent.name}_child_{parent_agent.id}"

    existing = db.query(Agent).filter(Agent.name == new_name).first()
    if existing:
        return None

    new_agent = Agent(
        name=new_name,
        type=parent_agent.type,
        owner_email=parent_agent.owner_email,
        generation=parent_agent.generation + 1
    )

    db.add(new_agent)
    db.commit()

    return new_agent


def decide_action(agent, db: Session):

    users_count = db.query(User).count()

    # =========================
    # META: CRIAÇÃO DE AGENTE
    # =========================
    if can_spawn(db, agent):
        new_agent = spawn_agent(db, agent)

        if new_agent:
            return f"spawned_{new_agent.name}"

    # =========================
    # GROWTH
    # =========================
    if agent.type == "growth":
        action = "incentivar_cadastro"

    # =========================
    # ANALYTICS
    # =========================
    elif agent.type == "analytics":
        action = f"analisar_total_usuarios_{users_count}"

    # =========================
    # OPS
    # =========================
    elif agent.type == "ops":
        pending = db.query(Task).filter(Task.status == "pending").count()

        if pending > 5:
            action = "priorizar_execucao"
        else:
            action = "monitorar_fila"

    else:
        return "idle"

    task = Task(
        agent_name=agent.name,
        action=action,
        owner_email=agent.owner_email
    )

    db.add(task)
    db.commit()

    return action