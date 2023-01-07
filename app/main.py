from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from typing import List


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    return


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existed_user = db.query(models.Post).filter(models.User.email == user.email).first()
    if existed_user:
        raise HTTPException(status_code=409, detail="This email has been used")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return
