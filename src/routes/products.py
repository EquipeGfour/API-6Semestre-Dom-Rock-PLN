from fastapi import APIRouter, Query
from modules.controllers.products import ProductsController

router = APIRouter()

@router.get("/genres")
def get_gender_review_count_by_age_range_and_product(product_id: int):
    gender_review_count = ProductsController().get_gender_count_by_age_range( product_id)
    return gender_review_count

@router.get("/get_summary")
def get_summary_by_product (product_id: int):
    summary = ProductsController().generate_summarization_by_product(product_id)
    return summary