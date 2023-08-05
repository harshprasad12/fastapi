from typing import Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/blog')
def test(limit: int, published: Optional[bool]= False):
    if published:
        print(published,"pub")
        return {"check": f'{limit} is the key'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



class Blog(BaseModel):
    title: str
    name: str
    published: Optional[bool] 

@app.post("/postest")
def postest(blog: Blog):
    return {"data": f'blog is created with title as {blog.title} and name {blog.name}'}