from src.face_detector import FaceDetector
from src.embedding_gen import EmbeddingGenerator
import os
import numpy as np

USER_IMG_PATH = r"inferencing\test.jpg"
USER_IMG_SAVE_PATH = r"inferencing"

class Inferencer():
    def __init__(self, use_pca=False, pca_save_dir=None):
        """
        use_pca: Whether to use PCA reduced embeddings or not
        pca_save_dir: Directory to saved PCA model
        """

        print("Loading FaceDetector and EmbeddingGenerator")
        self.facedectector_model = FaceDetector()
        self.embedding_model = EmbeddingGenerator(use_pca=use_pca, pca_save_dir=pca_save_dir)
        print("Loading clusters and cluster to images mapping")
        self.clusters = np.load("saved_cluster/clusters.npy")
        self.cluster_to_images = np.load("saved_cluster/clustermapping.npy", allow_pickle=True).item()
        
        if use_pca:
            print("Loading reduced dataset embeddings")
            self.dataset_embeddings = np.load("embeddings/reduced_embeddings.npy")
        else:
            print("Loading original dataset embeddings")
            self.dataset_embeddings = np.load("embeddings/embeddings.npy")

    def process_image(self):
        """
        Detect and extract user face from image. The cropped face is saved in the same directory as the input image
        and will be deleted after inference.

        Returns:
            Path of cropped face
        """

        print("Cropping and saving user face")
        try:
            cropped_face_path = self.facedectector_model.save_cropped_face(USER_IMG_PATH, USER_IMG_SAVE_PATH)
            return cropped_face_path
        except Exception as e:
            print(f"Error in cropping face: {e}")
            return None
        
    def find_cluster(self, cropped_face_path):
        """
        Generates embedding for user face and finds the cluster to which the user face belongs by comparing distance

        Args:
            cropped_face_path: Path of cropped face
        
        Returns:
            images which contain the user face
        """

        print("Generating embedding for user face")
        user_face_embedding = self.embedding_model.inference_embedding(cropped_face_path)
        os.remove(cropped_face_path)

        print("Finding cluster of user face")
        # find centroids of clusters
        unique_clusters = np.unique(self.clusters)
        cluster_centroids = {}

        for cluster in unique_clusters:
            if cluster != -1:
                cluster_embeddings = self.dataset_embeddings[self.clusters == cluster]
                centroid = np.mean(cluster_embeddings, axis=0)
                cluster_centroids[cluster] = centroid

        # find distance of user face from cluster centroids
        nearest_cluster = None
        nearest_cluster_distance = float('inf')

        for cluster, centroid in cluster_centroids.items():
            distance = np.linalg.norm(user_face_embedding - centroid)
            if distance < nearest_cluster_distance:
                nearest_cluster_distance = distance
                nearest_cluster = cluster

        if nearest_cluster == -1:
            return "User face does not belong to any cluster"
        else:
            person_in_images = self.cluster_to_images[nearest_cluster]
            image_name = [x.split("_")[0] for x in person_in_images]
            print(f"User face belongs to cluster {nearest_cluster} with images {image_name}")
            return image_name
        
    def delete_test_image(self):
        """
        Delete the test image after inference
        """
        os.remove(USER_IMG_PATH)

