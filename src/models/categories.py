from sqlalchemy import TIMESTAMP, Column, Integer, String
from models.base_class import Base
from sqlalchemy.sql import func

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
