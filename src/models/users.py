from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from models.base_class import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(50), nullable=False)
    senha = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
