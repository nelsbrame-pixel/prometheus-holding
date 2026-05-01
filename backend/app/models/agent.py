from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    type = Column(String)
    owner_email = Column(String)

    generation = Column(Integer, default=1)
    active = Column(Boolean, default=True)  # ← GOVERNANÇA