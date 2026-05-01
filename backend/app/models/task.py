from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action = Column(String)
    status = Column(String, default="pending")  # pending, running, done
    result = Column(String, nullable=True)