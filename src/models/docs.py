from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base_class import Base

class Docs(Base):
    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    document_name = Column(String(255), nullable=False)
    size = Column(String(50), nullable=False)
    uploaded_at = Column(TIMESTAMP, nullable=False, default=func.now())
    link = Column(String(255), nullable=False)