from .. import db_models, response_schemas, utils
from ..database import get_db
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags= ["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=response_schemas.UserCreateResponse)
def create_user(user: response_schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = db_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=response_schemas.UserCreateResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID: {id} does not exist",
        )

    return user
