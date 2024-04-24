from models.categories import Categories
from schemas.schemas import CategoryInput
from sqlalchemy.orm import Session
from fastapi import HTTPException


class CategoriesController:
    def create_category(self, data:CategoryInput,db: Session ):
        new_category = Categories(
            category = data.category
            )
        db.add(new_category)
        db.commit()
        db.refresh(new_category) 
        return new_category


    def get_category_id(self, category_id: int, db: Session):
        cat = db.query(Categories).filter(Categories.id == category_id).first()
        if cat is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return cat


    def get_category(self, db: Session):
        cat = db.query(Categories).all()
        if cat is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return cat
