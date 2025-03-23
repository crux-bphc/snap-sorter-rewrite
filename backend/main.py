import os
import dotenv
dotenv.load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from api import db_models
from api.database import engine, session_local
from api.routers import inferencing, auth, dashboard, profile
from datetime import datetime, timedelta, timezone


db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
#app = FastAPI()

app.mount("/static", StaticFiles(directory="clusters"), name="static")
app.mount("/images", StaticFiles(directory="data/images"), name="images")

origins = origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)


app.include_router(auth.router)
app.include_router(inferencing.router)
app.include_router(dashboard.router)
app.include_router(profile.router)


ZIP_SAVE_DIRECTORY = os.path.join("zip_files")

def cleanup_zip_files():
    db = session_local()
    try:
        five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
        old_records = db.query(db_models.ZipFileRecord).all()

        for record in old_records:
            record_time = record.timestamp.astimezone(timezone.utc)

            if record_time < five_minutes_ago:
                if os.path.exists(record.file_path):
                    os.remove(record.file_path)
                db.delete(record)
                print(f"Cleaned {len(old_records)} old zip files")
            else:
                print(f"No old zip files")

        db.commit()
    
    except Exception as e:
        print(e)
        db.rollback()

    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_zip_files, "interval", minutes = 4, id="cleanup_job", replace_existing=True)
scheduler.start()


app.add_event_handler("shutdown", scheduler.shutdown)


@app.get("/")
def read_root():
    return {"Hello": "World"}

