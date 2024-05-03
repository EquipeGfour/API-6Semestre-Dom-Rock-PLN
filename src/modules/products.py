from models.products import Products
from fastapi import HTTPException
from db.db import SessionLocal

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

