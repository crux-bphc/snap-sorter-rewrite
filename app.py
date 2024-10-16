from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from src.inference_pipeline import Inferencer

app = Flask(__name__)

inferencer = Inferencer(use_pca=True, pca_save_dir=r"pca_model")
images_folder = r"data\images"

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
            inferencer.delete_test_image()
            found_in_images = [url_for('serve_image', filename=i) for i in image_names]
            return render_template('result.html', image_names=found_in_images)
    return redirect(request.url)

@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(images_folder, filename)

if __name__ == "__main__":
    app.run(debug=True)
