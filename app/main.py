from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts/{id}")
def get_one_post(id):
    return id


@app.post("/posts")
def create_posts(post: Post):
    return {"payload": post}
