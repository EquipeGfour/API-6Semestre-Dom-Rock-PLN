from models.datasets import Datasets
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal


class DatasetsController:
    def __init__(self) -> None:
        self._db = SessionLocal()
    def create_dataset(self, data):
        self._db = SessionLocal()
        new_doc = Datasets(document_name = data.name,size = data.size,link = data.link)
        self._db.add(new_doc)
        self._db.commit()
        return {"message": "Document created successfully"}


    def get_dataset_id(self, dataset_id: int):
        self._db = SessionLocal()
        doc = self._db.query(Datasets).filter(Datasets.id == dataset_id).first()
        
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc


    def get_datasets(self):
        self._db = SessionLocal()
        doc = self._db.query(Datasets).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Documents not found")
        return doc
