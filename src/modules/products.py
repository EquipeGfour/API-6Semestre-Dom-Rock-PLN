from models.products import Products
from fastapi import HTTPException
from db.db import SessionLocal


class ProductsController:
    def create_product(self, name: str, product_id: int, brand: str, category_id: int):
        db = SessionLocal()
        new_product = Products(
            name=name,
            product_id=product_id,
            id_category=category_id,
            brand=brand
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {"message": "Product data inserted successfully"}

    def get_all_products(self):
        db = SessionLocal()
        return db.query(Products).all()

    def get_product_by_id(self, product_id: int):
        db = SessionLocal()
        product = db.query(Products).filter(Products.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

