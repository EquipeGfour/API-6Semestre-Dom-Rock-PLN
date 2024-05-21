from db.db import SessionLocal
from fastapi import HTTPException
from models.datasets import Datasets
from models.preprocessing_historics import PreprocessingHistorics
from typing import List
from json import dumps


class PreProcessing:
    def insert_register(self, dataset_id: int, preprocessing_dict: dict ):
        try:
            db = SessionLocal() 
            dataset = db.query(Datasets).filter(Datasets.id == dataset_id).first()
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
            db.add(new_preprocessing)
            db.commit()
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - PreProcessing >> Fail to inset proccess into database, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()



    def get_register(self, dataset_id: int):
        db = SessionLocal()
        doc = db.query(Datasets).filter(Datasets.id == dataset_id).first()
        preprocessings = db.query(PreprocessingHistorics).filter(PreprocessingHistorics.dataset_id == dataset_id).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return preprocessings


    def save_proccess_list(self, preprocessing_list: List[dict]):
        try:
            db = SessionLocal()
            preprocessing_objects = list()

            for item in preprocessing_list:
                dataset_id = item["dataset_id"]
                review_id = item["review_id"]
                del item["dataset_id"]
                del item["review_id"]
                preprocessing_objects.append(
                    PreprocessingHistorics(
                        input=item["original_doc"],
                        output=dumps(item),
                        dataset_id=dataset_id,
                        review_id=review_id,
                    )
                )
            db.bulk_save_objects(preprocessing_objects)
            db.commit()
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - PreProcessing >> Fail to save list of proccess, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()