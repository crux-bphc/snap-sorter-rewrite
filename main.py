import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import db_models
from api.database import engine
from api.routers import inferencing, user, auth

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="clusters"), name="static")
app.mount("/images", StaticFiles(directory="data/images"), name="images")

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(inferencing.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

