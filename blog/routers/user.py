from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi import FastAPI
from blog import hashing, models, schemas, database
from blog.database import get_db
from blog.repository import user
from blog.routers import oauth2


# subapi = FastAPI()
# @subapi.get("/sub")


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

get_db = database.get_db

@router.post("/", response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)


@router.get("/{id}", response_model=schemas.ShowUserDetail, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db), get_current_user_detail: schemas.User = Depends(oauth2.get_current_user)):
    return user.show(id,db,get_current_user_detail)