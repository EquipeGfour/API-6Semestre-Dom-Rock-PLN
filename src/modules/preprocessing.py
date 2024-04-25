from db.db import SessionLocal
from fastapi import HTTPException
from models.datasets import Datasets
from models.preprocessing_historics import PreprocessingHistorics



class PreProcessing:
    def __init__(self) -> None:
        self._db = SessionLocal()

    def insert_register(self, dataset_id: int, preprocessing_dict: dict ):
        self._db = SessionLocal()
        try:
            dataset = self._db.query(Datasets).filter(Datasets.id == dataset_id).first()
            if dataset is None:
                raise HTTPException(status_code=404, detail="Document not found")
            new_preprocessing = PreprocessingHistorics(
                input=preprocessing_dict["input"],
                output=preprocessing_dict["output"],
                step=preprocessing_dict["step"],
                dataset_id=dataset_id,
                processing_time=preprocessing_dict["time"],
                #review_id=preprocessing_dict["review_id"],
            )
            self._db.add(new_preprocessing)
            self._db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



    def get_register(self, dataset_id: int):
        self._db = SessionLocal()
        doc = self._db.query(Datasets).filter(Datasets.id == dataset_id).first()
        preprocessings = self._db.query(PreprocessingHistorics).filter(PreprocessingHistorics.dataset_id == dataset_id).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return preprocessings
