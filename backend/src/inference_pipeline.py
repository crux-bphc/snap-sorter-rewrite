from src.face_detector import FaceDetector
from src.embedding_gen import EmbeddingGenerator
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

USER_IMG_SAVE_PATH = r"inferencing"

class Inferencer():
    def __init__(self, use_pca=True):
        """
        use_pca: Whether to use PCA reduced embeddings or not
        pca_save_dir: Directory to saved PCA model
        """

        print("Loading FaceDetector and EmbeddingGenerator")
        self.facedectector_model = FaceDetector()
        self.embedding_model = EmbeddingGenerator(use_pca=use_pca)
        print("Loading clusters and cluster to images mapping")
        self.clusters = []
        self.cluster_to_images = []
        for x in sorted(os.listdir("saved_cluster")):
            self.clusters.append(np.load(os.path.join("saved_cluster", x, "clusters.npy")))
            self.cluster_to_images.append(np.load(os.path.join("saved_cluster", x, "clustermapping.npy"), allow_pickle=True).item())
        print(sorted(os.listdir("saved_cluster")))
        
        if use_pca:
            print("Loading reduced dataset embeddings")
            self.dataset_embeddings = []
            for x in sorted(os.listdir("embeddings")):
                self.dataset_embeddings.append(np.load(os.path.join("embeddings", x, "reduced_embeddings.npy")))
            print(sorted(os.listdir("embeddings")))
            self.path_to_pca_models = []
            for x in sorted(os.listdir("pca_model")):
                self.path_to_pca_models.append(os.path.join("pca_model", x))
            print(sorted(os.listdir("pca_model")))
        else:
            print("Loading original dataset embeddings")
            self.dataset_embeddings = []
            for x in sorted(os.listdir("embeddings")):
                self.dataset_embeddings.append(np.load(os.path.join("embeddings", x, "embeddings.npy")))
            print(sorted(os.listdir("embeddings")))


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
        
    def find_cluster(self, cropped_face_path):
        """
        Generates embedding for user face and finds the cluster to which the user face belongs by comparing distance

        Args:
            cropped_face_path: Path of cropped face
        
        Returns:
            images which contain the user face
        """

        high_confidence_result = []
        intermediate_confidence_result = {} #dictionary to store intermediate confidence images along with its day number and cluster number
        clustering_results = {
            "cluster_numbers": [],
            "similarity_scores": []
        }

        for i in range(len(self.clusters)):
            print("Generating embedding for user face")
            self.embedding_model.load_pca_model(self.path_to_pca_models[i])
            user_face_embedding = self.embedding_model.inference_embedding(cropped_face_path)

            print("Finding cluster of user face")
            # find centroids of clusters
            unique_clusters = np.unique(self.clusters[i])
            cluster_centroids = {}

            for cluster in unique_clusters:
                if cluster != -1:
                    cluster_embeddings = self.dataset_embeddings[i][self.clusters[i] == cluster]
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
                #return "User face does not belong to any cluster"
                print("User face does not belong to any cluster")
            else:
                person_in_images = self.cluster_to_images[i][nearest_cluster]
                image_name = [x.split("_face")[0] for x in person_in_images]
                print(f"User face belongs to cluster {nearest_cluster} in day {i + 1} with images {image_name}")
                clustering_results["cluster_numbers"].append(int(nearest_cluster))

                #computing average similarity score of user face with cluster images to use it as a threshold to determine
                #if user face is in Day-wise cluster or not

                cluster_embeddings = self.dataset_embeddings[i][self.clusters[i] == nearest_cluster]
                similarity_scores = cosine_similarity(user_face_embedding, cluster_embeddings)

                avg_similarity_score = np.mean(similarity_scores)
                print(f"Average similarity score with cluster images: {avg_similarity_score}")
                clustering_results["similarity_scores"].append(round(float(avg_similarity_score), 5))

                # TODO: keep 70% as threshold and for threshold between 60 to 70, prompt the user to choose
                if avg_similarity_score > 0.7:
                    high_confidence_result.extend(image_name)
                elif avg_similarity_score > 0.6:
                    intermediate_confidence_result[i + 1] = {
                    "cluster": int(nearest_cluster), # if this shit is not converted to python int, it raises JSON not serializable in API
                    "images": image_name
                }
                    
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