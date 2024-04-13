from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Text, Integer, Float
from models.base_class import Base
from sqlalchemy.sql import func


class Preprocessing(Base):
    __tablename__ = 'preprocessing'
    id = Column(Integer, primary_key=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    step = Column(String(255), nullable=False)
    doc_id = Column(ForeignKey('docs.id'), nullable=False)
    processing_time = Column(Float, nullable=False)
    error = Column(Text, nullable=False)
    review_id = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
