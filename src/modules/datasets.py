from models.datasets import Datasets
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal


class DatasetsController:
    def create_dataset(self, data):
        db = SessionLocal()
        new_doc = Datasets(document_name = data.name,size = data.size,link = data.link)
        db.add(new_doc)
        db.commit()
        db.close()
        return {"message": "Document created successfully"}


    def get_dataset_id(self, dataset_id: int):
        try:
            db = SessionLocal()
            doc = db.query(Datasets).filter(Datasets.id == dataset_id).first()
            if doc is None:
                raise HTTPException(status_code=404, detail="Document not found")
            return doc
        except Exception as e:
            msg = f"[ERROR] - DatasetsController >> Fail to retrieve database with id {dataset_id}, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()


    def get_datasets(self):
        db = SessionLocal()
        doc = db.query(Datasets).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Documents not found")
        return doc
