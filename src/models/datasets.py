from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base_class import Base

class Datasets(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    size = Column(String(50), nullable=False)
    link = Column(String(255), nullable=False)
    number_of_records = Column(Integer, nullable=True)
    uploaded_at = Column(TIMESTAMP, nullable=False, default=func.now())
