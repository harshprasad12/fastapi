from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# from pydantic import PostgresDsn

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'  #real                       ##### for sqlite ####
# SQLALCHEMY_DATABASE_URL = 'postgresql://harsh:harsh@localhost/Blog'  #real
# postgres://harsh.prasad:lquQItrUn35X@ep-shiny-bread-80247598.ap-southeast-1.aws.neon.tech/neondb  #change

# username= "harsh.prasad" #changeee
# password= "lquQItrUn35X"
# host= "ep-shiny-bread-80247598.ap-southeast-1.aws.neon.tech"
# database_name= "neondb"  #changeee


# from core.config import settings
# SQLALCHEMY_DATABASE_URL = "postgresql://harsh:harsh@postgresserver/db"


# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})  #real     ##### for sqlite ####
# database_url = f"postgresql+psycopg2://{username}:{password}@{host}/{database_name}"  #changeee
# engine = create_engine(database_url, echo=True)  #changeee

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal = sessionmaker(bind=engine) #for postgreSQL  #changeee   ##### for sqlite ####


# Base = declarative_base()                     ##### for sqlite ####

# def get_db():                                ##### for sqlite ####
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()                          ##### for sqlite ####




class DatabaseError(Exception):
    def __init__(self, detail: str = "Database error"):
        self.detail = detail
        super().__init__(self.detail)

try: 
    SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'  #real
    engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})  #real
    SessionLocal = sessionmaker(bind=engine) #for postgreSQL  #changeee
    Base = declarative_base()

    def get_db():
        db=SessionLocal()
        try:
            yield db
        finally:
            db.close()

except SQLAlchemyError as e:
    raise DatabaseError(detail="Database connection error") from e