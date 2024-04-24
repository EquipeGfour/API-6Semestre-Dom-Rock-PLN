from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base_class import Base


class Corpus(Base):
    __tablename__ = 'corpus'
    id = Column(Integer, primary_key=True)
    corpus = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
