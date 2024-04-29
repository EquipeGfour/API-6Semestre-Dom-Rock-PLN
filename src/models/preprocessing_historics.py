from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Text, Integer, Float
from models.base_class import Base
from sqlalchemy.sql import func


class PreprocessingHistorics(Base):
    __tablename__ = 'preprocessing_historics'
    id = Column(Integer, primary_key=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    dataset_id = Column(ForeignKey('datasets.id'), nullable=False)
    review_id = Column(ForeignKey('reviews.id'), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
