from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.user import User
from ..models.task import Task
from ..models.agent_log import AgentLog


def get_best_action(db, agent_name):
    results = (
        db.query(
            AgentLog.action,
            func.avg(AgentLog.score).label("avg_score")
        )
        .filter(AgentLog.agent_name == agent_name)
        .group_by(AgentLog.action)
        .order_by(func.avg(AgentLog.score).desc())
        .all()
    )

    if results:
        return results[0].action

    return None


def decide_action(agent, db: Session):

    users_count = db.query(User).count()

    best_action = get_best_action(db, agent.name)

    # =========================
    # GROWTH
    # =========================
    if agent.type == "growth":

        if best_action == "criou_task_growth":
            action = "incentivar_cadastro"

        else:
            action = "incentivar_cadastro"

        task = Task(
            agent_name=agent.name,
            action=action,
            owner_email=agent.owner_email
        )
        db.add(task)
        db.commit()

        return "criou_task_growth"


    # =========================
    # ANALYTICS
    # =========================
    if agent.type == "analytics":

        action = f"analisar_total_usuarios_{users_count}"

        task = Task(
            agent_name=agent.name,
            action=action,
            owner_email=agent.owner_email
        )
        db.add(task)
        db.commit()

        return action


    # =========================
    # OPS
    # =========================
    if agent.type == "ops":

        pending = db.query(Task).filter(Task.status == "pending").count()

        if pending > 5:
            action = "priorizar_execucao"
        else:
            action = "monitorar_fila"

        task = Task(
            agent_name=agent.name,
            action=action,
            owner_email=agent.owner_email
        )
        db.add(task)
        db.commit()

        return action

    return "idle"