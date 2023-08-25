from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from blog import database, hashing, models, schemas
from sqlalchemy.orm import Session
from blog.hashing import Hash
from blog.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    tags=["Authentication"]
    )

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email==request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Username')
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Incorrect Password')

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}       