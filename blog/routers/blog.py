from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from blog import models, schemas, database
from blog.database import get_db
from blog.repository import blog
from blog.routers import oauth2

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

get_db = database.get_db

@router.get("/", status_code=status.HTTP_200_OK)
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id,db,get_current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.BlogBase, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id,request,db,get_current_user)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, response, db, get_current_user)

@router.post("/users/")
def create_user_blog(request: schemas.BlogBase, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request,db,get_current_user)

@router.get("/users/blogs/")
def get_users_with_same_content(title: str, body: str, db: Session = Depends(get_db)):
    return blog.same_content(title, body, db)
