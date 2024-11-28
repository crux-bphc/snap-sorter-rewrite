import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api import oauth2, db_models
from src.inference_pipeline import Inferencer
from api.database import get_db

router = APIRouter()

inferencer = Inferencer(use_pca=True)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_CLUSTER_PATH = os.path.join(BASE_DIR, "clusters")
STATIC_BASE_URL = "http://127.0.0.1:8000/static"

def update_user_images(db: Session, user_id: int, image_names: list[str]):
    image_ids = []
    for image_name in image_names:
        image = db.query(db_models.Image).filter(db_models.Image.image_name == image_name).first()
        image_ids.append(image.id)

    try:
        db.execute(
            db_models.user_images.delete().where(db_models.user_images.c.user_id == user_id)
        )
        db.commit()
        db.refresh(db_models.user_images)
        for image_id in image_ids:
            db.execute(
                db_models.user_images.insert().values(user_id=user_id, image_id=image_id)
            )
    except Exception as e:
        print("No images found for the user, adding new ones")
        for image_id in image_ids:
            db.execute(
                db_models.user_images.insert().values(user_id=user_id, image_id=image_id)
            )
    db.commit()

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload JPG or PNG.")
    
    USER_IMG_PATH = os.path.join(BASE_DIR, "inferencing", "test.jpg")
    os.makedirs(os.path.dirname(USER_IMG_PATH), exist_ok=True)
    with open(USER_IMG_PATH, "wb") as image_handle:
        image_handle.write(file.file.read())

    cropped_face_path = inferencer.process_image()
    if not cropped_face_path:
        raise HTTPException(status_code=400, detail="No face detected in the uploaded image. Try again.")
    
    response = inferencer.find_cluster(cropped_face_path)
    inferencer.delete_test_image(cropped_face_path)

    if response["intermediate_confidence"]:
        response["message"] = "We need a bit of help to identify you in the following images."
        if len(response["high_confidence"]) > 0:
            update_user_images(db, current_user.id, response["high_confidence"])
    else:
        update_user_images(db, current_user.id, response["high_confidence"])
        response["message"] = None

    return JSONResponse(content=response)

@router.post("/cluster_samples")
async def get_cluster_samples(
    intermediate_confidence_data: dict,
    current_user: int = Depends(oauth2.get_current_user),
):
    response_data = {}

    for key, value in intermediate_confidence_data.items():
        cluster_path = os.path.join(BASE_CLUSTER_PATH, f"clusters_D{key}", str(value["cluster"]))
        if not os.path.exists(cluster_path) or not os.listdir(cluster_path):
            raise HTTPException(status_code=404, detail=f"No images found in {cluster_path}")

        first_image = os.listdir(cluster_path)[0]
        image_url = f"{STATIC_BASE_URL}/clusters_D{key}/{value['cluster']}/{first_image}"
        response_data[key] = {
            "cluster": value["cluster"],
            "image_url": image_url,
        }

    return response_data
