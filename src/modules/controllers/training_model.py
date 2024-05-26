from sqlalchemy import desc
from models.training_model import TrainingModel
from models.lexico import LexicoModel
from db.db import SessionLocal
from json import dumps



class TrainingModelController:
    def create_trainingModel(self, training_model: dict, lexico: dict):
        db = SessionLocal()
        try:
            new_lexico = LexicoModel(lexico=dumps(lexico))
            db.add(new_lexico)
            db.commit()
            db.refresh(new_lexico)
            new_Training_model = TrainingModel(
                name=training_model["name"],
                link=training_model["link"],
                path=training_model["path"],
                lexico_id=new_lexico.id  
            )
            db.add(new_Training_model)
            db.commit()
            db.refresh(new_Training_model)
            return {"message": "Training_model data inserted successfully"}
        finally:
            db.close()  


    def get_latest_training_model_with_lexico(self):
        db = SessionLocal()
        try:
            latest_training_model = db.query(TrainingModel).order_by(desc(TrainingModel.id)).first()
            if not latest_training_model:
                return {
                    "training_model": {},
                    "lexico": {}
                }
            lexico = db.query(LexicoModel).filter(LexicoModel.id == latest_training_model.lexico_id).first()
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