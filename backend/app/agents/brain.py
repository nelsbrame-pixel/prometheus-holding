from sqlalchemy.orm import Session
from ..models.user import User
from ..models.task import Task


def decide_action(agent, db: Session):

    users_count = db.query(User).count()

    # AGENTE DE CRESCIMENTO
    if agent.type == "growth":
        if users_count < 10:
            task = Task(
                agent_name=agent.name,
                action="incentivar_cadastro",
                owner_email=agent.owner_email
            )
            db.add(task)
            db.commit()
            return "criou_task_growth"

    # AGENTE ANALÍTICO
    if agent.type == "analytics":
        task = Task(
            agent_name=agent.name,
            action=f"analisar_total_usuarios_{users_count}",
            owner_email=agent.owner_email
        )
        db.add(task)
        db.commit()
        return "criou_task_analytics"

    # AGENTE OPERACIONAL
    if agent.type == "ops":
        pending_tasks = db.query(Task).filter(Task.status == "pending").count()

        if pending_tasks > 5:
            task = Task(
                agent_name=agent.name,
                action="priorizar_execucao",
                owner_email=agent.owner_email
            )
            db.add(task)
            db.commit()
            return "criou_task_ops"

    return "idle"