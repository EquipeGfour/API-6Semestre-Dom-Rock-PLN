from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Text
from models.base_class import Base
from sqlalchemy.sql import func


class ProcessData(Base):
    __tablename__ = 'process_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    preprocessing_id = Column(ForeignKey('preprocessing_historics.id'), nullable=False)
    review_id = Column(ForeignKey('reviews.id'), nullable=False)
    data = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())