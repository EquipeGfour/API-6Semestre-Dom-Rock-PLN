from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from models.base_class import Base
from sqlalchemy.sql import func


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    review = Column(String(800), nullable=False)
    rating = Column(Integer, nullable=False)
    recommend_product = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
    product_id = Column(ForeignKey('products.id'), nullable=True)
    reviewer_id = Column(ForeignKey('reviewers.id'), nullable=True)
