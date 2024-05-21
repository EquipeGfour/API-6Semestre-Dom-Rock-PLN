from sqlalchemy import TIMESTAMP, Column, Integer, Text
from models.base_class import Base
from sqlalchemy.sql import func

class LexicoModel(Base):
    __tablename__ = 'lexico'
    id = Column(Integer, primary_key=True)
    lexico = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
