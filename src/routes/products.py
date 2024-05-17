from fastapi import APIRouter, Query
from modules.products import ProductsController

router = APIRouter()

@router.get("/genres")
def get_gender_review_count_by_age_range_and_product(product_id: int, age_range: str = Query(..., description="Age range in the format 'min_age-max_age'")):
    gender_review_count = ProductsController.get_gender_count_by_age_range(age_range, product_id)
    return gender_review_count