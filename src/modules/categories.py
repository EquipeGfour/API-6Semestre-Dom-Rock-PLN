from models.categories import Categories
from fastapi import HTTPException
from db.db import SessionLocal
from typing import Union


class CategoriesController:
    def create_category(self, category: str):
        try:
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
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - CategoriesController >> Fail to insert category, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()


    def get_category_by_name(self, category: str) -> Union[Categories, None]:
        try:
            db = SessionLocal()
            cat = db.query(Categories).filter(Categories.category == category).first()
            if cat is None:
                return None
            return cat
        except Exception as e:
            msg = f"[ERROR] - CategoriesController >> Fail to get category {category}, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()


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
