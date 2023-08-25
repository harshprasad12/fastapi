import asyncio
import time
from fastapi import Depends, HTTPException, status, Response, FastAPI
from sqlalchemy.orm import Session
from blog import models, schemas
from blog.schemas import UserDetail, BlogResponse
import logging

# logging.basicConfig(
#     level=logging.INFO, 
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
logger = logging.getLogger(__name__) 

def get_all(db: Session):
    blogs_with_users = []
    blogs = db.query(models.Blog).all()

    for blog in blogs:
        blog_data = BlogResponse(id=blog.id, title=blog.content.title, body=blog.content.body)
        user_data = UserDetail(id=blog.user.id, name=blog.user.name, email=blog.user.email)
        blogs_with_users.append({"blog": blog_data.dict(), "user": user_data.dict()})
        logger.info(f"Processed blog {blog.id}")

    return blogs_with_users

def create(request: schemas.Blog, db: Session,get_current_user):
    logger.info("Creating a new blog...")

    user_id_object = db.query(models.User).filter(models.User.email==get_current_user.email)
    user_id = user_id_object.first().id
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_blog = db.query(models.BlogContent).filter(
        models.BlogContent.title == request.title,
        models.BlogContent.body == request.body,
    ).all()
    for blog in existing_blog:
        if blog.blogs[0].user_id == user_id:
            raise HTTPException(status_code=400, detail="Blog with same title and body already exists")

    new_blog = models.BlogContent(title=request.title, body=request.body)
    db.add(new_blog)
    new_user_blog = models.Blog(user_id=user_id, content=new_blog)
    db.add(new_user_blog)
    db.commit()
    db.refresh(new_blog)
    db.refresh(new_user_blog)

    logger.info("Blog created successfully")

    return {"message": "Blog created successfully"}


def destroy(id: int, db: Session,get_current_user):
    logger.info(f"Destroying blog with ID {id}...")

    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        logger.error(f"Blog with ID {id} not found")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    if (blog.first().user.email != get_current_user.email):
        logger.error(f"User attempted to delete a blog that doesn't belong to them (Blog ID: {id})")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Please enter the blog id that belongs to you')
    
    blog_content_delete = db.query(models.BlogContent).filter(models.BlogContent.title==blog.first().content.title, models.BlogContent.body==blog.first().content.body)
    blog.delete(synchronize_session=False)
    blog_content_delete.delete(synchronize_session=False)
    db.commit()
    logger.info(f"Blog with ID {id} destroyed successfully")

    return "Deleted"

def update(id:int, request: schemas.BlogBase, db: Session, get_current_user):
    logger.info(f"Received update_blog request for blog_id: %s", id)
    
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    blogs_to_update = db.query(models.Blog).join(models.BlogContent).filter(
        models.BlogContent.title == request.title,
        models.BlogContent.body == request.body
    ).all()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    if (blog.user.email != get_current_user.email):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Please enter the blog id that belongs to you')
    
    if not blogs_to_update:
        logger.warning("No blogs found to update with title: %s and body: %s", request.title, request.body)
        raise HTTPException(status_code=404, detail="Blogs not found")
    
    updated_blogs = []

    for blog in blogs_to_update:
        blog.content.title = request.title
        blog.content.body = request.body

        updated_blogs.append({
            "id": blog.id,
            "title": blog.content.title,
            "body": blog.content.body
        })

    db.commit()
    db.refresh(blog.content)

    logger.info("Updated %s blogs with title: %s and body: %s", len(updated_blogs), request.title, request.body)

    return updated_blogs


    # blog.content.title = request.title
    # blog.content.body = request.body
    
    # db.commit()
    # db.refresh(blog.content)

    # updated_blog = {
    #     "id": blog.id,
    #     "title": blog.content.title,
    #     "body": blog.content.body
    # }

    # return updated_blog

    # print(blog,"dsd")            ####  before  ######
    # blog.update(request.dict())
    # db.commit()
    # return "updated model"    ####  before  ######


def show(id: int, db:Session, get_current_user):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
    if get_current_user.email!=user.email:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail=f'Please enter correct id that belongs to you')
    return user 


def same_content(title, body, db):
    users = (
        db.query(models.User.id, models.User.name, models.User.email)
        .join(models.Blog, models.User.id == models.Blog.user_id)
        .join(models.BlogContent, models.Blog.content_id == models.BlogContent.id)
        .filter(models.BlogContent.title == title)
        .filter(models.BlogContent.body == body)
        .all()
    )

    users_dict_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
    return users_dict_list