from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api import oauth2, db_models, response_schemas
from api.database import get_db


router = APIRouter(
    tags=["Dashboard Endpoints"]
)

@router.get("/announcements", response_model= response_schemas.AnnouncementsResponse)
async def get_announcements(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Returns the latest 5 announcements in descending order
    """
    announcements_object = db.query(db_models.Announcements).order_by(db_models.Announcements.id.desc()).limit(5).all()
    response = {}
    response["announcements"] = [announcement.announcement for announcement in announcements_object]

    return response


@router.get("/stats", response_model=response_schemas.StatsResponse)
async def get_stats(
    db: Session = Depends(get_db),
):
    """
    Returns stats
    """
    users = db.query(db_models.User).count()
    images = db.query(db_models.Image).count()
    events = db.query(db_models.Event).count()
    inference_count = db.query(db_models.UserFaceAndResult).count()
    zip_files = db.query(db_models.ZipFileRecord).count()

    response = {
        "total_users": users,
        "total_images": images,
        "total_events": events,
        "inference_count": inference_count,
        "zip_files": zip_files
    }

    return response