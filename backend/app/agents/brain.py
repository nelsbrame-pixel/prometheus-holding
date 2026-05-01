from sqlalchemy.orm import Session
from ..models.user import User
from ..models.task import Task
from ..models.agent_log import AgentLog


def recent_action_exists(db, agent_name, action):
    last = db.query(AgentLog).filter(
        AgentLog.agent_name == agent_name,
        AgentLog.action == action
    ).order_by(AgentLog.id.desc()).first()

    if not last:
        return False

    return True


def decide_action(agent, db: Session):

    users_count = db.query(User).count()

    # =========================
    # AGENTE GROWTH
    # =========================
    if agent.type == "growth":

        if users_count < 10 and not recent_action_exists(
            db, agent.name, "criou_task_growth"
        ):
            task = Task(
                agent_name=agent.name,
                action="incentivar_cadastro",
                owner_email=agent.owner_email
            )
            db.add(task)
            db.commit()
            return "criou_task_growth"

        return "idle_growth"


    # =========================
    # AGENTE ANALYTICS
    # =========================
    if agent.type == "analytics":

        action_name = f"criou_task_analytics_{users_count}"

        if not recent_action_exists(db, agent.name, action_name):
            task = Task(
                agent_name=agent.name,
                action=f"analisar_total_usuarios_{users_count}",
                owner_email=agent.owner_email
            )
            db.add(task)
            db.commit()
            return action_name

        return "idle_analytics"


    # =========================
    # AGENTE OPS
    # =========================
    if agent.type == "ops":

        pending_tasks = db.query(Task).filter(
            Task.status == "pending"
        ).count()

        if pending_tasks > 5 and not recent_action_exists(
            db, agent.name, "criou_task_ops"
        ):
            task = Task(
                agent_name=agent.name,
                action="priorizar_execucao",
                owner_email=agent.owner_email
            )
            db.add(task)
            db.commit()
            return "criou_task_ops"

        return "idle_ops"

    return "idle"