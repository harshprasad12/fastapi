from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from blog import hashing, models, schemas
from blog.schemas import UserResponse, BlogResponse
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
logger = logging.getLogger(__name__)

def create(request: schemas.User, db:Session):
    user = db.query(models.User).filter(models.User.email==request.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User with this email already exists')
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)) #changed user_id
    
    logger.info(f"User created with name: %s", new_user.name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(user_id: int, db:Session, get_current_user):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} does not exist')
    if get_current_user.email!=user.email:
        raise HTTPException (status_code=status.HTTP_403_FORBIDDEN, detail=f'Please enter correct id that belongs to you')

    user_response = UserResponse(name=user.name, email=user.email)

    for blog in user.blogs:
        blog_response = BlogResponse(id=blog.id, title=blog.content.title, body=blog.content.body)
        user_response.blogs.append(blog_response)

    return user_response