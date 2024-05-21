from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from models.base_class import Base
from sqlalchemy.sql import func



class TrainingModel(Base):
    __tablename__ = 'training_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    link = Column(String(100), nullable=False)
    path = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    lexico_id = Column(ForeignKey('lexico.id'), nullable=False)

