from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from models.base_class import Base
from sqlalchemy.sql import func

class SubCategories(Base):
    __tablename__ = 'subcategories'
    id = Column(Integer, primary_key=True)
    id_category = Column(ForeignKey('categories.id'), nullable=False)
    subcategory = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())