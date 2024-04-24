from models.subcategories import SubCategories
from schemas.schemas import SubCategoryInput
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal


class SubCategoriesController:
    def create_subcategory(self, subcategory_data: SubCategoryInput):
        db = SessionLocal()
        try:
            subcategory = SubCategories(
                id_category=subcategory_data.id_category,
                subcategory=subcategory_data.subcategory
            )
            db.add(subcategory)
            db.commit()
            db.refresh(subcategory)
            return subcategory
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()


    def get_subcategory_data_by_id(self, subcategory_id: int):
        db = SessionLocal()
        subcategory_data = db.query(SubCategories).filter(SubCategories.id == subcategory_id).first()
        
        if subcategory_data is None:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        
        return subcategory_data


    def get_all_subcategory_datas(self):
        db = SessionLocal()
        datas = db.query(SubCategories).all()
        if datas is None:
            raise HTTPException(status_code=404, detail="Subcategorys not found")
        return datas

