from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from src.inference_pipeline import Inferencer
import pandas as pd

app = Flask(__name__)

inferencer = Inferencer(use_pca=True)
images_folder = r"data\images"
image_to_drive_id_mapping = pd.read_csv(r"imagedata.csv")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file.save("inferencing/test.jpg")
        cropped_face_path = inferencer.process_image()
        if cropped_face_path is not None:
            image_names = inferencer.find_cluster(cropped_face_path)
            #image_names is a list of image names
            drive_IDs = []
            for image_name in image_names:
                drive_IDs.append(image_to_drive_id_mapping[image_to_drive_id_mapping['image_name'] == image_name]['image_id'].values[0])
            inferencer.delete_test_image(cropped_face_path)
            drive_links = [f"https://drive.google.com/file/d/{file_id}/view" for file_id in drive_IDs]
            image_and_links = zip(image_names, drive_links)
            #found_in_images = [url_for('serve_image', filename=i) for i in image_names]
            #return render_template('result.html', image_names=found_in_images)
            return render_template('drive_view.html', image_and_links=image_and_links)
    return redirect(request.url)

@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(images_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
