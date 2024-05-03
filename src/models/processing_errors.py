from sqlalchemy import Column, Integer, String, Date, ForeignKey
from models.base_class import Base
from datetime import datetime

class ProcessingError(Base):
    __tablename__ = 'processing_errors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_preprocessing = Column(ForeignKey('preprocessing_historics.id'), nullable=False)
    error = Column(String(45), nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.now)
