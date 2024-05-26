from fastapi import APIRouter, HTTPException
from modules.controllers.training_model import TrainingModelController
from schemas.schemas import TrainingModelInput
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post("/create", description="Rota para inserir o treinamento dos modelos e o léxico")
def insert_training_model(training_model_data: TrainingModelInput):
    try:
        result = TrainingModelController().create_trainingModel(training_model_data)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/latest_with_lexico", description="Rota para obter o último modelo de treinamento juntamente com os dados do léxico associado")
def get_latest_training_model_with_lexico():
    try:
        result = TrainingModelController().get_latest_training_model_with_lexico()
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

