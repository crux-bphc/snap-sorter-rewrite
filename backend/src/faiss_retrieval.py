import faiss
import numpy as np
import os
from sklearn.metrics.pairwise import pairwise_distances, cosine_similarity
from src.embedding_gen import EmbeddingGenerator
import hdbscan
import json


class FaissRetriever():
    def __init__(self):
        print("FAISS retriever initializing")
        self.embedder = EmbeddingGenerator(use_pca=False)
    

    def create_faiss_index(self, embedding_path, faces_path, save_path):
        embeddings_faiss = np.load(os.path.join(embedding_path,"embeddings.npy")).astype(np.float32)
        embeddings_faiss /= np.linalg.norm(embeddings_faiss, axis=1, keepdims=True)

        index = faiss.IndexFlatIP(embeddings_faiss.shape[1])
        index.add(embeddings_faiss)

        image_paths = [os.path.basename(x) for x in sorted(os.listdir(faces_path))]

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        faiss_save_path = os.path.join(save_path, "faiss_index.bin")
        faiss.write_index(index, faiss_save_path)
        
        with open(os.path.join(save_path, "image_paths.json"), 'w') as f:
            json.dump(image_paths, f)
        
        print("FAISS index created and saved")


    def retrieve_images(self, faiss_index_event_path, query_image_path, threshold=0.70):
        index = faiss.read_index(os.path.join(faiss_index_event_path, "faiss_index.bin"))
        image_paths = json.load(open(os.path.join(faiss_index_event_path, "image_paths.json"), 'r'))

        query_embedding = self.embedder.inference_embedding(query_image_path).astype(np.float32)
        query_embedding /= np.linalg.norm(query_embedding)

        D, I = index.search(query_embedding.reshape(1, -1), k=int(len(image_paths)*0.1))

        filtered_indices = [idx for idx, score in zip(I[0], D[0]) if score >= threshold]
        filtered_embeddings = np.load(os.path.join(faiss_index_event_path, "embeddings.npy"))[filtered_indices]
        filtered_image_paths = [image_paths[idx] for idx in filtered_indices]

        # print scores and rank for filtered images
        for i, (idx, score) in enumerate(zip(I[0], D[0])):
            if score >= threshold:
                print(f"Rank: {i}, Image: {image_paths[idx]}, Score: {score}")

        if len(filtered_embeddings) == 0:
            print("No matches found above the similarity threshold.")
            return None
        else:

            print("Performing HDBSCAN clustering")
            distance_matrix = pairwise_distances(filtered_embeddings, metric="cosine").astype(np.float64)
            clusterer = hdbscan.HDBSCAN(min_cluster_size=3, min_samples=1, metric="precomputed", allow_single_cluster=True)
            cluster_labels = clusterer.fit_predict(distance_matrix)
            print(cluster_labels)

            query_similarities = cosine_similarity(query_embedding.reshape(1, -1), filtered_embeddings)[0]
            best_match_idx = np.argmax(query_similarities)
            best_match_cluster = cluster_labels[best_match_idx]

            cluster_images = [filtered_image_paths[i].split("_face")[0] for i, label in enumerate(cluster_labels) if label == best_match_cluster]
            print(cluster_images)
            return cluster_images
        
# fr = FaissRetriever()
# fr.retrieve_images(r"faiss_indexes/batchsnaps24", r"./inferencing\user_1_1736956554.jpg_face.jpg", threshold=0.70)