import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api import oauth2, db_models, response_schemas
from src.inference_pipeline import Inferencer
from api.database import get_db
import time

router = APIRouter(
    tags=["Core Functionality and Inferencing"]
)

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

def update_user_results(db: Session, user_id: int, user_face_path: str, clustering_results: dict):
    if clustering_results:
        user_cluster_data = db_models.UserFaceAndResult(
            user_id=user_id,
            user_face_path=user_face_path,
            clusters=clustering_results["cluster_numbers"],
            confidences=clustering_results["similarity_scores"]
        )
        db.add(user_cluster_data)
        db.commit()
        print("User results have been updated in the database.")


@router.post("/upload", response_model=response_schemas.UploadImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Upload an image file for inferencing and clustering. The image is processed and the response contains the high confidence images
    and intermediate confidence data. Intermediate confidence contains the day number as a key and the cluster number and images in that
    cluster as the value.
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload JPG or PNG.")
    
    USER_IMG_PATH = os.path.join(BASE_DIR, "inferencing", f"user_{current_user.id}_{int(time.time())}.jpg")
    os.makedirs(os.path.dirname(USER_IMG_PATH), exist_ok=True)
    with open(USER_IMG_PATH, "wb") as image_handle:
        image_handle.write(file.file.read())

    cropped_face_path = inferencer.process_image(USER_IMG_PATH)
    if not cropped_face_path:
        inferencer.delete_test_image(USER_IMG_PATH, None)
        raise HTTPException(status_code=400, detail="No face detected in the uploaded image. Try again.")
    
    response, clustering_results = inferencer.find_cluster(cropped_face_path)

    update_user_results(db, current_user.id, cropped_face_path, clustering_results)

    inferencer.delete_test_image(USER_IMG_PATH, cropped_face_path)

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
    """
    Gets the sample images for the clusters in the intermediate confidence data. It takes the entire intermediate confidence data
    in the request body and returns the sample image URL for each cluster along with the images in that cluster.
    """
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
    """
    Updates the selected images for the user in the database. It takes the list of selected image names in the request body and
    updates the user's images in the database.
    """
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
    """
    Gets the image URLs of the images found for the user in the database. It returns the image URLs in the response.
    """
    user_images = db.query(db_models.user_images).filter(db_models.user_images.c.user_id == current_user.id).all()
    image_data = {}
    for user_image in user_images:
        image = db.query(db_models.Image).filter(db_models.Image.id == user_image.image_id).first()
        if image:
            image_data[image.image_name] = {
                "image_url": f"{IMAGES_BASE_URL}/{image.image_name}",
                "image_drive_id": f"https://drive.google.com/file/d/{image.image_id_drive}/view"
            }
                    
    
    return {"images" :image_data}