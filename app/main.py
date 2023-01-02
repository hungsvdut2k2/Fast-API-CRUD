from fastapi import FastAPI, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool


try:
    conn = psycopg2.connect(
        host='localhost', database='Fast_API', user='postgres', password='Hung18062002', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
except:
    print("Error")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    sql = 'SELECT * FROM posts'
    cursor.execute(sql)
    posts = cursor.fetchall()
    return {"posts": posts}


@app.get("/posts/{id}")
def get_one_post(id: int):
    sql = f"SELECT * FROM posts WHERE id = {str(id)}"
    cursor.execute(sql)
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    sql = f'INSERT INTO posts (title, content, published) VALUES {post.title, post.content, post.published}'
    cursor.execute(sql)
    conn.commit()
    return {}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    return


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    sql = f"DELETE FROM posts WHERE id = {str(id)} RETURNING *"
    cursor.execute(sql)
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    return {}
