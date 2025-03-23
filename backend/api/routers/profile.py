import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from api import oauth2, db_models, response_schemas
from api.database import get_db
import zipfile
from datetime import datetime, timezone

router = APIRouter(
    tags=["Profile Endpoints"]
)

@router.get("/profile", response_model=response_schemas.ProfileResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Returns the user's profile information and whether a zip download is available or not
    """
    user = db.query(db_models.User).filter(db_models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    zip_record = db.query(db_models.ZipFileRecord).filter(db_models.ZipFileRecord.user_id == current_user.id).first()
    download_available = True if zip_record else False
    response = {
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
        "download_available": download_available
    }

    return response


IMAGE_DIRECTORY = os.path.join("data", "images")
ZIP_SAVE_DIRECTORY = os.path.join("zip_files")

@router.post("/request_download", response_model=response_schemas.RequestDownloadResponse)
async def request_download(
    events: List[int],
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Creates a zip file of the images found for the user in the specified events and returns a message
    """
    os.makedirs("zip_files", exist_ok=True)
    record = db.query(db_models.ZipFileRecord).filter(db_models.ZipFileRecord.user_id == current_user.id).first()
    if record:
        response = {
            "message": "You have already requested a download. You can request a new download after 5 minutes. Visit the Profile section to download the file."
        }
        return response
    else:
        user_images = db.query(db_models.user_images).filter(db_models.user_images.c.user_id == current_user.id,
                                                         db_models.user_images.c.false_positive == False).all()
        
        image_paths = []
        for user_image in user_images:
            image = db.query(db_models.Image).filter(db_models.Image.id == user_image.image_id,
                                                     db_models.Image.event_id.in_(events)).first()
            if image:
                image_paths.append(os.path.join(IMAGE_DIRECTORY, image.image_name))
        
        if not image_paths:
            raise HTTPException(
                status_code=404,
                detail="No images found for the user"
            )
        
        os.makedirs(ZIP_SAVE_DIRECTORY, exist_ok=True)
        zip_file_name = f"{current_user.email}.zip"
        zip_file_path = os.path.join(ZIP_SAVE_DIRECTORY, zip_file_name)
        with zipfile.ZipFile(zip_file_path, "w") as zip_file:
            for image_path in image_paths:
                zip_file.write(image_path, os.path.basename(image_path))
        
        record = db_models.ZipFileRecord(user_id=current_user.id, file_path=zip_file_path, timestamp=datetime.now(timezone.utc))
        db.add(record)
        db.commit()
        db.refresh(record)

        response = {
            "message": "Your download will be available in the Profile section once ready."
        }

        return response

        
@router.get("/download_zip", response_class=FileResponse)
async def download_zip(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    """
    Downloads the zip file created for the user if available
    """
    record = db.query(db_models.ZipFileRecord).filter(db_models.ZipFileRecord.user_id == current_user.id).first()
    if not record or not os.path.exists(record.file_path):
        raise HTTPException(
            status_code=404,
            detail="No download request found"
        )
    
    return FileResponse(
        path=record.file_path, 
        filename=os.path.basename(record.file_path), 
        media_type="application/zip",  
        headers={"Cache-Control": "no-store, must-revalidate"}
    )