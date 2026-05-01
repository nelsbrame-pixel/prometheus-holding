from sqlalchemy import Column, Integer, String
from ..database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    owner_email = Column(String)