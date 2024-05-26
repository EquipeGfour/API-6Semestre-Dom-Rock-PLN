from models.products import Products
from models.reviewers import Reviewers
from models.reviews import Reviews
from fastapi import HTTPException
from db.db import SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
from models.preprocessing_historics import PreprocessingHistorics
from json import loads
from modules.pln.summary import Summary

class ProductsController:
    def __init__(self):
        self.summary = Summary()
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

    def get_gender_count_by_age_range(self, product_id: int):
        try:
            def calculate_age(birth_year: int) -> int:
                current_year = datetime.now().year
                return current_year - birth_year
            age_ranges = [
                (15, 30),
                (30, 45),
                (45, 60),
                (60, 100)  
            ]
            db = SessionLocal()
            reviewers = db.query(Reviewers).join(Reviews, Reviewers.id == Reviews.reviewer_id).filter(Reviews.product_id == product_id).all()
            gender_review_count = {
                'Feminino': [0, 0, 0, 0],
                'Masculino': [0, 0, 0, 0]
            }
            for reviewer in reviewers:
                reviewer_age = calculate_age(reviewer.birth_year)
                for idx, (min_age, max_age) in enumerate(age_ranges):
                    if min_age <= reviewer_age < max_age:
                        if reviewer.gender.lower() == 'm':
                            gender_review_count['Masculino'][idx] += 1
                        elif reviewer.gender.lower() == 'f':
                            gender_review_count['Feminino'][idx] += 1
                        break  
            return gender_review_count
        except Exception as e:
            msg = f"[ERROR] - ProductsController >> Failed to retrieve gender review count by age range: {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()

    def generate_summarization_by_product(self, product_id):
        db = SessionLocal()
        try:
            query_result = db.query(PreprocessingHistorics.output).\
                    join(Reviews, Reviews.id == PreprocessingHistorics.review_id).\
                    join(Products, Products.id == Reviews.product_id).\
                    filter(Products.id == product_id).all()
            reviews = []
            for review in query_result:
                reviews.append(loads(review[0]))
            ret = self.summary.sumary_extractive(reviews)
            return ret
        except Exception as e:
            msg = f"[ERROR] - ProductsController >> Failed to generate summarization by product: {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()

