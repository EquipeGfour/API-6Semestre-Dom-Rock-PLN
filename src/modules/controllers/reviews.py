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

    def insert_review(self, review_input: dict, reviewer_id:int, product_id:int):
        try:
            db = SessionLocal()

            recommend = self._evaluate_recomend_product(review_input["recommend_to_a_friend"])
            review = Reviews(
                title=review_input["review_title"],
                review=review_input["review_text"],
                rating=review_input["overall_rating"],
                recommend_product=recommend,
                reviewer_id=reviewer_id,
                product_id=product_id
            )
            db.add(review)
            db.commit()      
            db.refresh(review)                        
            return review
        except Exception as e: 
            msg = f'[ERROR] - ReviewsController >> fail to insert {str(e)}'
            print(msg)
            raise msg
        finally:
            db.close()


    def _evaluate_recomend_product(self, recommend:str):
        if recommend.lower() == "yes":
            return True
        else:
            return False
