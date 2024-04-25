from fastapi import APIRouter
from modules.preprocessing import PreProcessing
from modules.pipeline import pipeline


router = APIRouter()

@router.post("/start", description="Rota inserir iniciar o pré processamento")
def insert_preprocessing_register(dataset_id: int):
    return pipeline.start_pipeline(dataset_id)

