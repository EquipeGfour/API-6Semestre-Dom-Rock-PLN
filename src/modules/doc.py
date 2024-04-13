from models.docs import Docs
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal


class Doc:
    def __init__(self) -> None:
        self._db = SessionLocal()
    def create_doc(self, data):
        new_doc = Docs(document_name = data.name,size = data.size,link = data.link)
        self._db.add(new_doc)
        self._db.commit()
        return {"message": "Document created successfully"}


    def get_doc_id(self, doc_id: int):
        doc = self._db.query(Docs).filter(Docs.id == doc_id).first()
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc


    def get_doc(self):
        doc = self._db.query(Docs).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Documents not found")
        return doc
