from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Table
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
    user_data = relationship(
        "UserFaceAndResult", back_populates="user", cascade="all, delete-orphan"
    )


class UserFaceAndResult(Base):
    __tablename__ = "user_face_and_result"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_face_path = Column(String, nullable=False)
    clusters = Column(JSON, nullable=True)
    confidences = Column(JSON, nullable=True)

    user = relationship("User", back_populates="user_data")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    image_id_drive = Column(String, nullable=False)

    users_found_in = relationship(
        "User", secondary=user_images, back_populates="found_in_images"
    )
