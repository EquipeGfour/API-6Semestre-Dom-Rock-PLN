from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base_class import Base


class Lexicos(Base):
    __tablename__ = 'lexicos'
    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())