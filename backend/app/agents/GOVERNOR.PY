from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.agent import Agent
from ..models.agent_log import AgentLog


MIN_SCORE = 0.4
MAX_AGENTS = 10


def evaluate_agents(db: Session):
    agents = db.query(Agent).all()

    for agent in agents:
        avg_score = db.query(func.avg(AgentLog.score)).filter(
            AgentLog.agent_name == agent.name
        ).scalar()

        if avg_score is None:
            continue

        if avg_score < MIN_SCORE:
            agent.active = False

    db.commit()


def enforce_limits(db: Session):
    agents = db.query(Agent).order_by(Agent.id.asc()).all()

    if len(agents) <= MAX_AGENTS:
        return

    overflow = len(agents) - MAX_AGENTS

    for i in range(overflow):
        agents[i].active = False

    db.commit()