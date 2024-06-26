from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.db import SessionLocal
from models.reviewers import Reviewers
from schemas.schemas import ReviewerInput
from typing import Union

class ReviewerController:
    def create_reviewer(self, review: dict):
        try:
            reviewer_data = ReviewerInput(
                reviewer_id=review["reviewer_id"],
                birth_year=review["reviewer_birth_year"],
                gender=review["reviewer_gender"],
                state=review["reviewer_state"]
            )
            db = SessionLocal()
            reviewer = self.get_reviewer_by_id(reviewer_data.reviewer_id)
            if reviewer:
                return reviewer  
            new_reviewer = Reviewers(
                reviewer_id=reviewer_data.reviewer_id,
                birth_year=reviewer_data.birth_year,
                gender=reviewer_data.gender,
                state=reviewer_data.state
            )
            db.add(new_reviewer)
            db.commit()
            db.refresh(new_reviewer)
            return new_reviewer
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - ReviewerController >> Fail to insert reviewer into database, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()

    def get_reviewer_by_id(self, reviewer_id: str) -> Union[Reviewers, None]:
        db = SessionLocal()
        reviewer = db.query(Reviewers).filter(Reviewers.reviewer_id == reviewer_id).first()
        if reviewer is None:
            return None
        return reviewer

    def get_all_reviewers(self):
        db = SessionLocal()
        return db.query(Reviewers).all()

    def get_reviewer_by_id(self, reviewer_id: int):
        db = SessionLocal()
        return db.query(Reviewers).filter(Reviewers.id == reviewer_id).first()
