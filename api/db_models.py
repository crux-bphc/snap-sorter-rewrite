from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base


user_images = Table(
    "user_images",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    found_in_images = relationship(
        "Image", secondary=user_images, back_populates="users_found_in"
    )

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    
    users_found_in = relationship(
        "User", secondary=user_images, back_populates="found_in_images"
    )
