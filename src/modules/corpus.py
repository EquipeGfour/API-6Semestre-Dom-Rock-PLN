from models.corpus import Corpus
from schemas.schemas import CorpusInput
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db import SessionLocal


class CorpusController:
    def create_corpus(self, data:CorpusInput):
        try:
            db = SessionLocal()
            existing_corpus = db.query(Corpus).filter(Corpus.corpus == data.corpus).first()
            if existing_corpus:
                return existing_corpus  # Retorna o corpus existente se já estiver na base de dados
            new_corpus = Corpus(
                corpus=data.corpus
            )
            db.add(new_corpus)
            db.commit()
            return new_corpus
        except Exception as e:
            db.rollback()
            msg = f"[ERROR] - CorpusController >> Failed to insert corpus into database, {str(e)}"
            raise HTTPException(status_code=500, detail=msg)
        finally:
            db.close()

    def get_corpus_id(self, corpus_id: int, db: Session):
        lex = db.query(Corpus).filter(Corpus.id == corpus_id).first()
        if lex is None:
            raise HTTPException(status_code=404, detail="Corpus not found")
        return lex


    def get_corpus(self, db: Session):
        lex = db.query(Corpus).all()
        if lex is None:
            raise HTTPException(status_code=404, detail="Corpus not found")
        return lex
