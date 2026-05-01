from datetime import datetime
from sqlalchemy.orm import Session

from .brain import decide_action


def run_agent(agent, db: Session):
    action = decide_action(agent, db)

    return {
        "action": action,
        "result": "ok",
        "time": datetime.utcnow()
    }