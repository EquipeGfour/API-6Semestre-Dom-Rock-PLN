from sqlalchemy import TIMESTAMP, Column, Integer, String, Enum, Date, func
from models.base_class import Base


class Reviewers(Base):
    __tablename__ = 'reviewers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer_id = Column(String(75), nullable=False)
    birth_year = Column(Integer, nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    state = Column(String(45), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())
