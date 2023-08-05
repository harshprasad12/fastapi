from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from blog import hashing, models, schemas, database
from blog.database import get_db
from blog.repository import user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

get_db = database.get_db





@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # # hashed_password = pwd_cxt.hash(request.password)
    # new_user = models.User(name=request.name, email=request.email, password=hashing.bcrypt(request.password))
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user
    return user.create(request,db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.id==id).first()

    # if not user:
    #     raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f'User with the id {id} not found')
    # return user
    return user.show(id,db)