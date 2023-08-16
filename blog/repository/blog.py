import asyncio
import time
from fastapi import Depends, HTTPException, status, Response, FastAPI
from sqlalchemy.orm import Session
from blog import models, schemas

def get_all(db: Session):
    blogs= db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db: Session,get_current_user):
    user_id_object = db.query(models.User).filter(models.User.email==get_current_user.email)
    user_id = user_id_object.first().id
    new_blog = models.Blog(title= request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id: int, db: Session,get_current_user):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    if (blog.first().creator.email != get_current_user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Please enter the blog id that belongs to you')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"

def update(id:int, request: schemas.Blog, db: Session, get_current_user):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    if (blog.first().creator.email != get_current_user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Please enter the blog id that belongs to you')
    blog.update(request.dict())
    db.commit()
    return "updated model"

def show(id:int, response: Response, db: Session,get_current_user):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id {id} not found')
    if (blog.creator.email != get_current_user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Please enter the blog id that belongs to you')
    return blog
