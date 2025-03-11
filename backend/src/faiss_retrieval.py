import faiss
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from src.embedding_gen import EmbeddingGenerator
from sklearn.cluster import AgglomerativeClustering
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

        images_ranking = []
        for i, (idx, score) in enumerate(zip(I[0], D[0])):
            if score >= threshold:
                print(f"Rank: {i}, Image: {image_paths[idx]}, Score: {score}")
                images_ranking.append(image_paths[idx])
        print(images_ranking)
        

        if len(filtered_embeddings) == 0:
            print("No matches found above the similarity threshold.")
            return None
        else:

            print("Performing clustering")
            clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.3, metric='cosine', linkage='average')
            cluster_labels = clustering.fit_predict(filtered_embeddings)
            print(cluster_labels)
            print("[" + ", ".join([str(x) for x in cluster_labels]) + "]")

            query_similarities = cosine_similarity(query_embedding.reshape(1, -1), filtered_embeddings)[0]
            valid_clusters = set(cluster_labels) - {-1}
            if not valid_clusters:
                print("No valid clusters found, returning top-ranked images.")
                return [img.split("_face")[0] for img in filtered_image_paths]

            cluster_scores = {}
            for cluster in valid_clusters:
                cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster]
                cluster_similarities = query_similarities[cluster_indices]
                cluster_scores[cluster] = np.mean(cluster_similarities) * len(cluster_indices)

            best_match_cluster = max(cluster_scores, key=cluster_scores.get)
            print(f"Best cluster chosen: {best_match_cluster} with avg similarity: {cluster_scores[best_match_cluster]:.4f}")

            cluster_images = [
                filtered_image_paths[i].split("_face")[0]
                for i, label in enumerate(cluster_labels)
                if label == best_match_cluster
            ]

            print("\nFinal ranked images from best cluster:")
            for img in cluster_images:
                print(img)

            return cluster_images
        
# fr = FaissRetriever()
# fr.retrieve_images(r"faiss_indexes/batchsnaps24", r"./inferencing\user_1_1736956554.jpg_face.jpg", threshold=0.70)