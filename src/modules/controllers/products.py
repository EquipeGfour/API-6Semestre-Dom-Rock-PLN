from models.products import Products
from models.reviewers import Reviewers
from models.reviews import Reviews
from fastapi import HTTPException
from db.db import SessionLocal
from datetime import datetime

class ProductsController:
    def create_product(self, product: dict, category_id: int):
        try:
            db = SessionLocal()
            existing_product = db.query(Products).filter(Products.product_id == product["id"]).first()
            if existing_product:
                return  existing_product
            new_product = Products(
                name=product["name"],
                product_id=product["id"],
                id_category=category_id,
                brand=product["brand"]
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)
            return new_product
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - ProductsController >> Fail to inserto product into database, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()


    def get_all_products(self):
        db = SessionLocal()
        return db.query(Products).all()

    def get_product_by_id(self, product_id: int):
        db = SessionLocal()
        product = db.query(Products).filter(Products.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def get_gender_count_by_age_range(age_range: str, product_id: int):
        try:
            def calculate_age(birth_year: int) -> int:
                current_year = datetime.now().year
                age = current_year - birth_year
                return age
            
            db = SessionLocal()
            min_age, max_age = map(int, age_range.split('-'))
            reviewers = db.query(Reviewers).join(Reviews, Reviewers.id == Reviews.reviewer_id).filter(Reviews.product_id == product_id).all()
            print("Product ID:", product_id)
            print("Gender  Age")
            for reviewer in reviewers:
                reviewer_age = calculate_age(reviewer.birth_year)
                print(reviewer.gender, "   ", reviewer_age)
            
            gender_review_count = {'M': 0, 'F': 0}
            if not reviewers:
                # Se não houver revisores para o produto, retorne o dicionário vazio
                return gender_review_count
            
            for reviewer in reviewers:
                reviewer_age = calculate_age(reviewer.birth_year)
                if reviewer_age >= min_age and reviewer_age <= max_age:
                    if reviewer.gender == 'M':
                        gender_review_count['M'] += 1
                    elif reviewer.gender == 'F':
                        gender_review_count['F'] += 1
                        
            return gender_review_count
        except Exception as e:
            msg = f"[ERROR] - ProductsController >> Failed to retrieve gender review count by age range: {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()




