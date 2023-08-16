import time
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, FastAPI
from sqlalchemy.orm import Session
from blog import models, schemas, database
from blog.database import get_db, engine
from fastapi.middleware.cors import CORSMiddleware
from blog.repository import blog
from blog.routers import oauth2
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

get_db = database.get_db
@router.get("/", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request,db,get_current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id,db,get_current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db,get_current_user)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, response, db, get_current_user)



