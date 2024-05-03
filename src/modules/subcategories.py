from models.subcategories import SubCategories
from schemas.schemas import SubCategoryInput
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal



class SubCategoriesController:
    def create_subcategory(self, subcategory: str, category_id: int):
        db = SessionLocal()
        try:
            subcat = self.get_subcategory_by_name(subcategory)
            if subcat:
                return subcat
            subcategory = SubCategories(
                id_category=category_id,
                subcategory=subcategory
            )
            db.add(subcategory)
            db.commit()
            db.refresh(subcategory)
            return subcategory
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - SubCategoriesController >> Fail to insert subcategory {subcategory} into database, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()


    def get_subcategory_by_name(self, subcategory: str):
        db = SessionLocal()
        subcat = db.query(SubCategories).filter(SubCategories.subcategory == subcategory).first()
        if subcat is None:
            return None
        return subcat


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

