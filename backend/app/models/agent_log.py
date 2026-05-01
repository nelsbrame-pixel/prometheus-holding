from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from ..database import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action = Column(String)
    result = Column(String)
    score = Column(Float, default=0.0)  # ← NOVO (avalia desempenho)
    timestamp = Column(DateTime, default=datetime.utcnow)