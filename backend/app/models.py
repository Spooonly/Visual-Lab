from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    reagents = Column(String)
    result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
