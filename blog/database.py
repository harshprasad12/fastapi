import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import HTTPException, status

# logging.basicConfig(level=logging.ERROR)
# from pydantic import PostgresDsn

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'  #real                       ##### for sqlite ####
# SQLALCHEMY_DATABASE_URL = 'postgresql://harsh:harsh@localhost/Blog'  #real
# postgres://harsh.prasad:lquQItrUn35X@ep-shiny-bread-80247598.ap-southeast-1.aws.neon.tech/neondb  #change

# username= "harsh.prasad" #changeee
# password= "lquQItrUn35X"
# host= "ep-shiny-bread-80247598.ap-southeast-1.aws.neon.tech"
# database_name= "neondb"  #changeee


# from core.config import settings
# SQLALCHEMY_DATABASE_URL = "postgresql://harsh:harsh@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})  #real     ##### for sqlite ####
# database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database_name}"  #changeee
# engine = create_engine(database_url, echo=True)  #changeee

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal = sessionmaker(bind=engine) #for postgreSQL  #changeee   ##### for sqlite ####


Base = declarative_base()                     ##### for sqlite ####

# def get_db():                                ##### for sqlite #####
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()                           ##### for sqlite #####




def get_db():
    try:
        db = SessionLocal()
        yield db
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Database down')
    finally:
        db.close()
        