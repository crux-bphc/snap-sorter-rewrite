from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import db_models, utils, oauth2, response_schemas

router = APIRouter(
    tags = ["Auth"]
)

@router.post("/login", response_model=response_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # create a token and return it
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}
    
