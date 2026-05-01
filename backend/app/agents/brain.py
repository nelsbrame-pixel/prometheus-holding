from sqlalchemy.orm import Session
from ..models.user import User
from ..models.task import Task

def decide_action(agent, db: Session):

    if agent.type == "growth":
        users_count = db.query(User).count()

        if users_count < 10:
            task = Task(
                agent_name=agent.name,
                action="incentivar_cadastro"
            )
            db.add(task)
            db.commit()
            return "task_criada"

    return "idle"