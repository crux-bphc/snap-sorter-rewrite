from face_detector import FaceDetector
from embedding_gen import EmbeddingGenerator
from clusterer import HDBSCANClusterer
from faiss_retrieval import FaissRetriever
import os

SNAPS_DIR = r"data\alpha"
FACES_SAVE_DIR = r"data\atmos25_faces"
EMBEDDING_SAVE_DIR = r"embeddings\embeddings_D6"
CLUSTER_SAVE_DIR = r"saved_cluster\cluster_D6"
PCA_SAVE_DIR = r"pca_model\pca_D6"
CLUSTER_LOCAL_SAVE = r'clusters\clusters_D6'
FAISS_INDEX_SAVE_DIR = r"faiss_indexes\atmos25"

def face_detect(images_dir, save_face_dir):
    face_detector = FaceDetector()
    face_detector.detect_all_faces_and_save(images_dir, save_face_dir)

def generate_embeddings(faces_dir, save_embedding_dir, use_pca, pca_save_dir):
    embedding_generator = EmbeddingGenerator(use_pca=use_pca, pca_save_dir=pca_save_dir)
    embedding_generator.create_and_save_embeddings(faces_dir, save_embedding_dir)

def cluster_faces_HDBSCAN(faces_dir, save_cluster_dir, embeddings_folder, use_pca):
    clusterer = HDBSCANClusterer(faces_dir, save_cluster_dir, embeddings_folder, use_pca=use_pca)
    clusterer.fit_map_clusterer()
    clusterer.save_clusters_to_folder(CLUSTER_LOCAL_SAVE)

def make_faiss_index(embedding_path, faces_path, save_path):
    faiss_retriever = FaissRetriever()
    faiss_retriever.create_faiss_index(embedding_path, faces_path, save_path)


def main():
    #face_detect(SNAPS_DIR, FACES_SAVE_DIR)
    # generate_embeddings(FACES_SAVE_DIR, EMBEDDING_SAVE_DIR, use_pca=True, pca_save_dir=PCA_SAVE_DIR)
    #cluster_faces_HDBSCAN(FACES_SAVE_DIR, CLUSTER_SAVE_DIR, EMBEDDING_SAVE_DIR, use_pca=True)

    # emb = EmbeddingGenerator(n_components=40 ,use_pca=True, pca_save_dir=PCA_SAVE_DIR)
    # emb.apply_pca_on_exising_embeddings(r'embeddings\embeddings.npy', PCA_SAVE_DIR, EMBEDDING_SAVE_DIR)
    # make_faiss_index(EMBEDDING_SAVE_DIR, FACES_SAVE_DIR, FAISS_INDEX_SAVE_DIR)
    pass

if __name__ == "__main__":
    main()