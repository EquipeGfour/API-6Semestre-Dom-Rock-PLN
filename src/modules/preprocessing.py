from db.db import SessionLocal
from fastapi import HTTPException
from models.docs import Docs
from models.preprocessing import Preprocessing



class PreProcessing:
    def __init__(self) -> None:
        self._db = SessionLocal()

    def insert_register(self, doc_id: int, preprocessing_dict: dict ):
        try:
            doc = self._db.query(Docs).filter(Docs.id == doc_id).first()
            if doc is None:
                raise HTTPException(status_code=404, detail="Document not found")
            new_preprocessing = Preprocessing(
                input=preprocessing_dict["input"],
                output=preprocessing_dict["output"],
                step=preprocessing_dict["step"],
                doc_id=doc_id,
                processing_time=preprocessing_dict["time"],
                review_id=preprocessing_dict["review_id"],
                error=preprocessing_dict["error"]
            )
            self._db.add(new_preprocessing)
            self._db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



    def get_register(self, doc_id: int):
        doc = self._db.query(Docs).filter(Docs.id == doc_id).first()
        preprocessings = self._db.query(Preprocessing).filter(Preprocessing.doc_id == doc_id).all()
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return preprocessings
