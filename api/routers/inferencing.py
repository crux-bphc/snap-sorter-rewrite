import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api import oauth2, db_models, response_schemas
from src.inference_pipeline import Inferencer
from api.database import get_db

router = APIRouter()

inferencer = Inferencer(use_pca=True)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_CLUSTER_PATH = os.path.join(BASE_DIR, "clusters")
STATIC_BASE_URL = os.getenv("STATIC_BASE_URL")
IMAGES_BASE_URL = os.getenv("IMAGES_BASE_URL")


def update_user_images(db: Session, user_id: int, image_names: list[str], update: bool):
    if len(image_names) == 0:
        user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
        if user:
            user.found_in_images.clear()
            db.commit()
            print("Cleared all images for the user.")
        return

    image_ids = []
    for image_name in image_names:
        image = db.query(db_models.Image).filter(db_models.Image.image_name == image_name).first()
        if image:
            image_ids.append(image.id)

    try:
        if not update:
            user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
            if user:
                user.found_in_images.clear()
                print("Deleted all images for the user, adding new ones")

        user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
        if user:
            for image_id in image_ids:
                image = db.query(db_models.Image).filter(db_models.Image.id == image_id).first()
                if image:
                    if image not in user.found_in_images:
                        user.found_in_images.append(image)
            db.commit()
            print("New images have been added for the user.")
    except Exception as e:
        db.rollback()
        print("Error occurred while updating user images:", e)


@router.post("/upload", response_model=response_schemas.UploadImageResponse)
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
        update_user_images(db, current_user.id, response["high_confidence"], update=False)
    else:
        update_user_images(db, current_user.id, response["high_confidence"], update=False)
        response["message"] = None

    return response


@router.post("/cluster_samples", response_model=response_schemas.ClusterSamplesResponse)
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
            "sample_url": image_url,
            "images" : value["images"]
        }

    return response_data


@router.post("/update_user_selected_images")
async def update_user_selected_images(
    selected_images: List[str],
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    if selected_images:
        update_user_images(db, current_user.id, selected_images, update=True)
        return JSONResponse(content={"message": "Images updated successfully"})
    else:
        return JSONResponse(content={"message": "No images selected to update"})

@router.get("/get_user_results", response_model=response_schemas.UserResultsResponse)
async def get_user_results(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user_images = db.query(db_models.user_images).filter(db_models.user_images.c.user_id == current_user.id).all()
    image_urls = []
    for user_image in user_images:
        image = db.query(db_models.Image).filter(db_models.Image.id == user_image.image_id).first()
        image_urls.append(f"{IMAGES_BASE_URL}/{image.image_name}")
    
    return {"image_urls": image_urls}