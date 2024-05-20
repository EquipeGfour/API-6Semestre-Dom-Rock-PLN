from requests import Session
from sqlalchemy import desc
from schemas.schemas import LexicoInput, TrainingModelInput
from models.training_model import Training_model
from models.lexico import Lexico
from fastapi import Depends, HTTPException
from db.db import get_db, SessionLocal

class TrainingModelController:
    def create_trainingModel(self, TrainingModel_data):
        db = SessionLocal()
        try:
            new_lexico = Lexico(lexico=TrainingModel_data.lexico)
            db.add(new_lexico)
            db.commit()
            db.refresh(new_lexico)
            new_TrainingModel = Training_model(
                name=TrainingModel_data.name,
                link=TrainingModel_data.link,
                path=TrainingModel_data.path,
                lexico_id=new_lexico.id  
            )
            db.add(new_TrainingModel)
            db.commit()
            db.refresh(new_TrainingModel)
            return {"message": "Training_model data inserted successfully"}
        finally:
            db.close()  

    def get_latest_training_model_with_lexico(self):
        db = SessionLocal()
        try:
            latest_training_model = db.query(Training_model).order_by(desc(Training_model.id)).first()
            if not latest_training_model:
                return {
                    "training_model": {},
                    "lexico": {}
                }
            lexico = db.query(Lexico).filter(Lexico.id == latest_training_model.lexico_id).first()
            if not lexico:
                return {
                    "training_model": {
                        "id": latest_training_model.id,
                        "name": latest_training_model.name,
                        "link": latest_training_model.link,
                        "path": latest_training_model.path
                    },
                    "lexico": {}
                }
            return {
                "training_model": {
                    "id": latest_training_model.id,
                    "name": latest_training_model.name,
                    "link": latest_training_model.link,
                    "path": latest_training_model.path
                },
                "lexico": {
                    "id": lexico.id,
                    "lexico": lexico.lexico
                }
            }
        finally:
            db.close()