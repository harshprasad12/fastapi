from sqlalchemy import Column, Integer, String, ForeignKey, Table
from .database import Base
from sqlalchemy.orm import relationship


class BlogContent(Base):
    __tablename__ = 'blog_contents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

    blogs = relationship("Blog", back_populates="content")

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("blog_contents.id"))

    user = relationship("User", back_populates="blogs")
    content = relationship("BlogContent", back_populates="blogs")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blog", back_populates="user")