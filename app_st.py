import streamlit as st
from src.inference_pipeline import Inferencer
import os
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS

def correct_image_orientation(image):
    """Correct the orientation of the image based on EXIF data."""
    try:
        exif = image._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if TAGS.get(tag) == 'Orientation':
                    orientation = value
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
                    break
    except Exception as e:
        st.error(f"Error reading EXIF data: {e}")
    return image

def display_results(image_names_high_confidence):
    # Display matching images in a grid layout
    st.write("Matching Images:")
    
    columns_per_row = 4  # Number of images per row
    cols = st.columns(columns_per_row)

    if len(image_names_high_confidence) == 0:
        st.write("No matching images found. This could be because you were not present during batchsnaps or if you were in too few pictures.")
    else:
        for idx, image_name in enumerate(image_names_high_confidence):
            # Find the corresponding Drive ID from the CSV mapping
            drive_id_row = image_to_drive_id_mapping[image_to_drive_id_mapping['image_name'] == image_name]
            if not drive_id_row.empty:
                drive_id = drive_id_row.iloc[0]['image_id']
                drive_link = f"https://drive.google.com/file/d/{drive_id}/view"
                
                # Check if the image exists locally in the images_folder
                image_path = os.path.join(images_folder, image_name)
                with cols[idx % columns_per_row]:  # Place image in the correct column
                    if os.path.exists(image_path):
                        # Open and transpose image if needed
                        image = Image.open(image_path)
                        image = correct_image_orientation(image)
                        st.image(image, caption=image_name, use_column_width=True)
                        
                        # Button styled link
                        st.markdown(f"""
                            <a href="{drive_link}" target="_blank" style="
                                display: inline-block;
                                padding: 8px 16px;
                                margin-top: 8px;
                                background-color: #4285f4;
                                color: white;
                                text-align: center;
                                text-decoration: none;
                                border-radius: 4px;
                                font-weight: bold;
                            ">View on Google Drive</a>
                            """, unsafe_allow_html=True)
                    else:
                        st.write(f"{image_name}: [View on Google Drive]({drive_link})")

st.title("Snap Sorter (Beta)")
st.write("Upload your image to find all images you are present in.")

inferencer = Inferencer(use_pca=True)
image_to_drive_id_mapping = pd.read_csv(r"imagedata.csv")
images_folder = r"data/images"

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    os.makedirs("inferencing", exist_ok=True)
    USER_IMG_PATH = "inferencing/test.jpg"
    with open(USER_IMG_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    cropped_face_path = inferencer.process_image()
    
    if cropped_face_path is not None:
        st.write("Running inference...")

        image_names_high_confidence, image_names_intermediate_confidence = inferencer.find_cluster(cropped_face_path)
        inferencer.delete_test_image(cropped_face_path)

        # Check if intermediate confidence images are present
        if len(image_names_intermediate_confidence) > 0:
            st.write("We need a bit of help to identify you in the following images.")
            intermediate_confidence_sample_faces = {}
            for day_number, (cluster_id, image_names) in image_names_intermediate_confidence.items():
                path_to_cluster = os.path.join(r'clusters', f"clusters_D{day_number}", f"{cluster_id}")
                sample_path = os.walk(path_to_cluster).__next__()[2][0]
                intermediate_confidence_sample_faces[day_number] = os.path.join(path_to_cluster, sample_path)
            
            # Display intermediate confidence face samples in a grid layout
            cols = st.columns(len(intermediate_confidence_sample_faces))
            for idx, (day_number, sample_face_path) in enumerate(intermediate_confidence_sample_faces.items()):
                with cols[idx]:
                    sample_face = Image.open(sample_face_path)
                    sample_face = correct_image_orientation(sample_face)
                    st.image(sample_face, caption=f'Face {day_number}', use_column_width=True)
            
            # Add "None of these are me" as an option
            options = list(intermediate_confidence_sample_faces.keys()) + ["None of these are me"]
            selected_faces = st.multiselect("Select the face(s) that belong to you:", options)
            
            # Confirm selection to proceed
            if st.button("Confirm Selection"):
                if "None of these are me" in selected_faces:
                    st.write("Proceeding with high-confidence images only.")
                    display_results(image_names_high_confidence)
                else:
                    for day_number in selected_faces:
                        if day_number != "None of these are me":
                            image_names_high_confidence.extend(image_names_intermediate_confidence[day_number][1])
                    display_results(image_names_high_confidence)
        else:
            display_results(image_names_high_confidence)

    else:
        st.write("Error in processing the image. This could happen if the image does not contain a face or if the face is not detected properly. Upload another image to try again.")
