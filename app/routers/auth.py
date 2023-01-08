from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(tags=["Authencation"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail="Wrong Password")
    access_token = oauth2.create_access_token(data={"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
