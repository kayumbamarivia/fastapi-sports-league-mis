from sqlalchemy import JSON, Column, Integer, String
from config.database import Base

class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    coach = Column(String, unique=True, nullable=False)
    players = Column(JSON, unique=True, nullable=False)

