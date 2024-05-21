from models.users import Users
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from db.db import get_db
from schemas.schemas import UsersInput

class UsersController:
    def get_user(self, user_id: int, db: Session = Depends(get_db)):
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_all_users(self, db: Session):
        return db.query(Users).all()
    
    def insert_user(self, user_data: UsersInput, db: Session = Depends(get_db)):
        new_user = Users(
            name=user_data.name,
            senha=user_data.senha,
            email=user_data.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User data inserted successfully"}

    def update_user(self, user_id: int, user_data: UsersInput, db: Session = Depends(get_db)):
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for attr, value in user_data.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        db.commit()
        db.refresh(user)
        return {"message": "User data updated successfully"}

    def delete_user(self, user_id: int, db: Session = Depends(get_db)):
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}