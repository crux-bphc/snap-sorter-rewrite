from jose import JWTError, jwt
import datetime
from . import response_schemas, database, db_models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("OAUTH2_SECRET_KEY")
ALGORITHM = os.getenv("OAUTH2_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("OAUTH2_EXPIRATION_MINUTES"))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        token_data = response_schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate" : "Bearer"}
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(db_models.User).filter(db_models.User.id == token.id).first()

    return user
