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
    announcements_object = db.query(db_models.Announcements).order_by(db_models.Announcements.id.desc()).limit(5).all()
    response = {}
    response["announcements"] = [announcement.announcement for announcement in announcements_object]

    return response