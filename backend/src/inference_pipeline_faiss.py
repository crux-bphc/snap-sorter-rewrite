from src.face_detector import FaceDetector
from src.embedding_gen import EmbeddingGenerator
from src.faiss_retrieval import FaissRetriever
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

USER_IMG_SAVE_PATH = r"inferencing"

class Inferencer():
    def __init__(self):

        print("Loading FaceDetector, EmbeddingGenerator and FaissRetriever")
        self.facedectector_model = FaceDetector()
        self.embedding_model = EmbeddingGenerator(use_pca=False)
        self.faiss_retriever = FaissRetriever()


    def process_image(self, user_image_path):
        """
        Detect and extract user face from image. The cropped face is saved in the same directory as the input image
        and will be deleted after inference.

        Returns:
            Path of cropped face
        """

        print("Cropping and saving user face")
        try:
            cropped_face_path = self.facedectector_model.save_cropped_face(user_image_path, USER_IMG_SAVE_PATH)
            return cropped_face_path
        except Exception as e:
            print(f"Error in cropping face: {e}")
            return None
        
    def retrieve_images(self, cropped_face_path, threshold=0.70):
        """
        Generates embedding for user face and finds matching images

        Args:
            cropped_face_path: Path of cropped face
        
        Returns:
            images which contain the user face
        """

        high_confidence_result = []
        intermediate_confidence_result = {} #dictionary to store intermediate confidence images along with its day number and cluster number
        clustering_results = {
            "cluster_numbers": [0,0],
            "similarity_scores": [0,0]
        }

        events = os.listdir(r"faiss_indexes")
        for event_name in events:
            event_results = self.faiss_retriever.retrieve_images(os.path.join("faiss_indexes", event_name), cropped_face_path, threshold=threshold)
            if event_results:
                high_confidence_result.extend(event_results)
                    
        print(high_confidence_result)
        results = {
            "high_confidence": high_confidence_result,
            "intermediate_confidence": intermediate_confidence_result
        }
        return results, clustering_results
        
    def delete_test_image(self, user_image_path, cropped_face_path):
        """
        Delete the test image after inference
        """
        os.remove(user_image_path)
        #os.remove(cropped_face_path) #temporarily store cropped faces instead of embeddings