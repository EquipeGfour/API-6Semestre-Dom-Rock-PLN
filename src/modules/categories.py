from models.categories import Categories
from fastapi import HTTPException
from db.db import SessionLocal
from typing import Union


class CategoriesController:
    def create_category(self, category: str):
        db = SessionLocal()
        cat = self.get_category_by_name(category)
        if cat:
            return cat
        new_category = Categories(
            category = category
            )
        db.add(new_category)
        db.commit()
        db.refresh(new_category) 
        return new_category


    def get_category_by_name(self, category: str) -> Union[Categories, None]:
        db = SessionLocal()
        cat = db.query(Categories).filter(Categories.category == category).first()
        if cat is None:
            return None
        return cat


    def get_category_id(self, category_id: int):
        db = SessionLocal()
        cat = db.query(Categories).filter(Categories.id == category_id).first()
        if cat is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return cat


    def get_category(self):
        db = SessionLocal()
        cat = db.query(Categories).all()
        if cat is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return cat
