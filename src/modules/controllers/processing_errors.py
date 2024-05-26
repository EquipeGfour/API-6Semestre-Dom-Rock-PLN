from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.db import get_db
from models.processing_errors import ProcessingError
from schemas.schemas import ProcessingErrorInput

class ProcessingErrorController:
    def create_processing_error(self, error_data: ProcessingErrorInput, db: Session = Depends(get_db)):
        new_error = ProcessingError(
            id_preprocessing=error_data.id_preprocessing,
            error=error_data.error
        )
        db.add(new_error)
        db.commit()
        db.refresh(new_error)
        return new_error

    def get_all_processing_errors(self, db: Session = Depends(get_db)):
        return db.query(ProcessingError).all()

    def get_processing_error_by_id(self, error_id: int, db: Session = Depends(get_db)):
        return db.query(ProcessingError).filter(ProcessingError.id == error_id).first()
