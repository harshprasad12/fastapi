import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient
from .main import app  # Import your FastAPI app instance
from blog.database import get_db  # Import your database function
from blog.routers import oauth2  # Import your OAuth2 module
from blog import models, schemas  # Import your schema definitions
from blog.database import SessionLocal
class TestBlogEndpoint(unittest.TestCase):


    mock_blogs = [
    schemas.ShowBlog(title="new_title", body="new_body", creator=schemas.ShowUser(name='harsh', email='harsh@gmail.com')),
    ]
    # mock_blogs = [
    #         models.Blog(title="new_title", body="new_body", creator={"name":'harsh', "email":"harsh@gmail.com"})
    #     ]
    # print(mock_blogs,"dsdsssds")


#     class Blog:
#     def __init__(self, id, title, body):
#         self.id = id
#         self.title = title
#         self.body = body

# # Given mock_blogs list
# mock_blogs = [
#     Blog(id=1, title="Blog 1", body="Content 1"),
#     Blog(id=2, title="Blog 2", body="Content 2"),
# ]

# # Print the details of each blog
# for blog in mock_blogs:
#     print(f"Blog ID: {blog.id}")
#     print(f"Title: {blog.title}")
#     print(f"Body: {blog.body}")
#     print()  # Add an empty line for separation




    def setUp(self):
        self.client = TestClient(app)
        self.mock_db = Mock()



    def test_get_all_blogs(self):
        # Define a mock list of blogs to be returned by the mock database

        
        # Mock the database session and query to return the mock blogs
        mock_db_session = self.mock_db()
        mock_db_session.query.return_value.all.return_value = self.mock_blogs  
        print("dds")
        # Create a test request
        response = self.client.get("/blog")
        print(response,"dddadadada")
        # print(response.text)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        # response.headers["content-type"]="application/json"
        self.assertEqual(response.headers["content-type"], "application/json")

        returned_blogs = [schemas.ShowBlog(**blog) for blog in response.json()]
        # print(returned_blogs[0],"ddsfsdfsd")
        # print(returned_blogs,"ss")
        # for blog in self.mock_blogs:
        #     print(blog.creator,"hhhhh")
        # print(self.mock_blogs[1],"dsds")
        # print(self.mock_blogs.json(),"mb")
        if self.mock_blogs in returned_blogs:
            print("true")
        # self.assertEqual(len(returned_blogs), len(self.mock_blogs))

        for returned_blog, mock_blog in zip(returned_blogs, self.mock_blogs):
            print(mock_blog.creator)
            print(returned_blog.creator,"hsgag")
            # self.assertEqual(returned_blog["id"], self.mock_blogs.id)
            # self.assertEqual(returned_blog["title"], mock_blog.title)
            self.assertEqual(returned_blog.title, mock_blog.title)
            assert returned_blog.title == mock_blog.title, "Title does not match"
            self.assertEqual(returned_blog.body, mock_blog.body)
            self.assertEqual(returned_blog.creator, mock_blog.creator)


            # self.assertEqual(returned_blog["body"], mock_blog.body)

        # Assert that the database was queried correctly
        # mock_db_session.query.assert_called_once_with(models.Blog)
        # mock_db_session.query.assert_called_once_with(mock_blog)
        # mock_db_session.query.return_value.all.assert_called_once()

if __name__ == "__main__":
    unittest.main()