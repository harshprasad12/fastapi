# from blog.database import SessionLocal

####   Testt  ####
# import json
# from fastapi import Depends
# from fastapi.testclient import TestClient
# # from blog.main import app  # Import your FastAPI app instance here
# from .main import app
# import uuid
# from blog import database
# from sqlalchemy.orm import Session

# client = TestClient(app)
# # fake_collection=f"fake_{uuid.uuid4()}"
# from blog.database import get_db
# print(client,"client")
# def test_successful_login():
#     # Assuming valid user credentials
#     login_data = {
#         "username": "okk",
#         "password": "okk"
#     }
#     print(login_data,"ld")
#     response = client.post('/login', data=login_data)
#     # print(data,"data")
#     print(response.text,"response")
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


#####  test  #####

# test_successful_login()

# def test_invalid_username():
#     # Assuming an invalid username
#     login_data = {
#         "username": "nonexistent@example.com",
#         "password": "valid_password"
#     }
#     response = client.post("/login", data=login_data)
#     assert response.status_code == 404

# def test_incorrect_password():
#     # Assuming a valid username but incorrect password
#     login_data = {
#         "username": "valid@example.com",
#         "password": "wrong_password"
#     }
#     response = client.post("/login", data=login_data)
#     assert response.status_code == 403










# from fastapi.testclient import TestClient
# import pytest

# from blog.main import app
# from blog import models, schemas

# # Use a SQLite in-memory database for testing
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from blog.routers.oauth2 import get_current_user

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Set up the test client
# client = TestClient(app)

# # Fixture to create a testing database session
# @pytest.fixture(scope="module")
# def db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Mock get_current_user function for testing
# def mock_get_current_user():
#     return schemas.User(name="ok", email="ok", password="ok")

# def test_create_blog(db):
#     # Mock the get_current_user function
#     app.dependency_overrides[get_current_user] = mock_get_current_user
    
#     # Prepare test data
#     test_blog = {
#         "title": "Test Blog",
#         "body": "This is a test blog body."
#     }
    
#     # Send a POST request to the API
#     response = client.post("blog/users/blogs/", json=test_blog)
#     print(response,"sd")
    
#     # Check response status code
#     assert response.status_code == 200
    
#     # Check response content
#     assert response.json() == {"message": "Blog created successfully"}
    
#     # Check if the blog was actually added to the database
#     created_blog = db.query(models.BlogContent).filter(models.BlogContent.title == test_blog["title"]).first()
#     assert created_blog is not None
#     assert created_blog.body == test_blog["body"]
































from fastapi import Depends
from fastapi.testclient import TestClient
import urllib.parse

from pytest import Session
from blog import database
from blog.main import app

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# from blog.database import Base, get_db
# # from ..main import app, get_db
# ''
# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         print(db)
#         yield db
#     finally:
#         db.close()
# # print(get_db)

# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_init_user():
    data={
        "username": "ok",
        "password": "ok"
    }
    login_user = client.post('/login',data=data)
    token_data=login_user.json()
    print(token_data,"token_data")
    assert login_user.status_code == 200 , "response code returned is not 200"
    assert "access_token" in login_user.json() , "access_token key is not found in login api response"
    print(login_user.json(),"login_user")
