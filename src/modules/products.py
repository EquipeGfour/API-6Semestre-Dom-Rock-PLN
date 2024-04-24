from models.products import Products
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.db import get_db
from schemas.schemas import ProductsInput

class ProductsController:
    def create_product(self, product_data: ProductsInput, db: Session = Depends(get_db)):
        new_product = Products(
            name=product_data.name,
            product_id=product_data.product_id,
            id_category=product_data.id_category,
            brand=product_data.brand
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {"message": "Product data inserted successfully"}

    def get_all_products(self, db: Session):
        return db.query(Products).all()

    def get_product_by_id(self, product_id: int, db: Session):
        product = db.query(Products).filter(Products.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product