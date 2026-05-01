from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, default="generic")  # 👈 NOVO
    active = Column(Boolean, default=True)
    last_run = Column(String, nullable=True)