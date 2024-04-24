from db.db import SessionLocal
from models.reviews import Reviews
from fastapi import HTTPException
from schemas.schemas import ReviewInput



class ReviewsController:
    def get_all_reviews(self):
        db = SessionLocal()
        reviews = db.query(Reviews).all()
        return reviews

    def get_review_id(self, review_id: int):
        db = SessionLocal()
        review = db.query(Reviews).filter(Reviews.id == review_id).first()
        if review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return review

    def insert_review(self, review_input: ReviewInput):
        db = SessionLocal()
        recommend = self._evaluate_recomend_product(review_input.recomend_product)
        review = Reviews(
            title=review_input.title,
            review=review_input.review,
            rating=review_input.rating,
            recommend_product=recommend
        )
        db.add(review)
        db.commit()      
        db.refresh(review)                              
        return review

    def _evaluate_recomend_product(self, recommend:str):
        if recommend.lower() == "yes":
            return True
        else:
            return False
