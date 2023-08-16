from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from blog import hashing, models, schemas
from blog.routers import oauth2

def create(request: schemas.User, db:Session):
    user = db.query(models.User).filter(models.User.email==request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User with this email already exists')

    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)) #changed user_id
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db:Session, get_current_user):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
    if get_current_user.email!=user.email:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f'Please enter correct id that belongs to you')
    return user 