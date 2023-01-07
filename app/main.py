from fastapi import FastAPI, status, HTTPException, Depends
from .routers import post, user
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
