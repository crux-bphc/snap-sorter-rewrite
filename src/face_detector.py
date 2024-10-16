import mtcnn
import cv2
import os


class FaceDetector:
    '''
    FaceDetector class to detect all faces in images in a given directory

    args:
        directory: str: path to the directory containing images
        save_directory: str: path to the directory to save the cropped faces
    
    returns:
        None
    '''
    def __init__(self):
        print("FaceDetector object initializing")
        self.detector = mtcnn.MTCNN()
        print("FaceDetector initialized successfully")

    def detect_all_faces_and_save(self, directory, save_directory):
        '''
        Detects all faces in images in a given directory

        Args:
            directory: input directory of images
            save_directory: directory where faces will be saved
        '''
        images = os.listdir(directory)
        print(f"Found {len(images)} images in {directory}")

        for image in images:
            img = cv2.imread(os.path.join(directory, image))
            faces = self.detector.detect_faces(img)
            print(f"Detected {len(faces)} faces in {image}")
            for i, face in enumerate(faces):
                x, y, width, height = face['box']
                confidence = face['confidence']
                if confidence > 0.97:
                    face_img = img[y:y+height, x:x+width]
                    cv2.imwrite(os.path.join(save_directory, f"{image}_face{i}_{confidence:.2f}.jpg"), face_img)
                    print(f"Face {i} in {image} with confidence {confidence:.2f} saved successfully")

    def save_cropped_face(self, image_path, save_path):
        img = cv2.imread(image_path)
        face = self.detector.detect_faces(img)
        print(f"Detected {len(face)} faces in {image_path}")
        x, y, width, height = face[0]['box']
        face_cropped = img[y:y+height, x:x+width]
        cv2.imwrite(os.path.join(save_path, f"{os.path.basename(image_path)}_face.jpg"), face_cropped)
        return os.path.join(save_path, f"{os.path.basename(image_path)}_face.jpg")
