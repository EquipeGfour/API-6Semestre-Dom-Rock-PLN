from pydantic import BaseModel
from typing import Union, Optional


class InputDoc(BaseModel):
    name: str
    size: int
    link: str
    
    class Config:
        orm_mode = True

class PreprocessingInput(BaseModel):
    input:str
    output:str
    step:str
    processing_time:int

class CorpusInput(BaseModel):
    corpus:str

class UsersInput(BaseModel):
    name:str
    senha:str
    email:str
    userAdmin: Optional[bool] = False

class ReviewInput(BaseModel):
    title: str
    review: str
    rating: int
    recomend_product: str

class ProcessDataInput(BaseModel):
    review_id : Union[int, None]
    preprocessing_id : Union[int, None]
    data: str

class ProductsInput(BaseModel):
    id_category : Union[int, None]
    name:str
    product_id:str
    brand:str

class ProcessingErrorInput(BaseModel):
    id_preprocessing: int
    error: str

class ReviewerInput(BaseModel):
    reviewer_id: str
    birth_year: int
    gender: str
    state: str

class CategoryInput(BaseModel):
    category:str

class SubCategoryInput(BaseModel):
    id_category : Union[int, None]
    subcategory:str

class TrainingModelInput(BaseModel):
    name: str
    link: str
    path: str
    lexico: str = None 

class LexicoInput(BaseModel):
    lexico: str