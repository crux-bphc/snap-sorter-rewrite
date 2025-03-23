from sqlalchemy import JSON, Boolean, Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


user_images = Table(
    "user_images",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id"), primary_key=True),
    Column("false_positive", Boolean, default=False, nullable=False),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    
    found_in_images = relationship(
        "Image", secondary=user_images, back_populates="users_found_in"
    )
    user_data = relationship(
        "UserFaceAndResult", back_populates="user", cascade="all, delete-orphan"
    )
    zip_files = relationship("ZipFileRecord", back_populates="user", cascade="all, delete-orphan")


class UserFaceAndResult(Base):
    __tablename__ = "user_face_and_result"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_face_path = Column(String, nullable=False)

    user = relationship("User", back_populates="user_data")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    image_name = Column(String, nullable=False)
    image_id_drive = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)

    users_found_in = relationship(
        "User", secondary=user_images, back_populates="found_in_images"
    )
    event = relationship("Event", back_populates="images")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    event_name = Column(String, nullable=False, unique=True)

    images = relationship("Image", back_populates="event")


class Announcements(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, nullable=False)
    announcement = Column(String, nullable=False)


class ZipFileRecord(Base):
    __tablename__ = "zip_files"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="zip_files")
