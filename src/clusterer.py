from sklearn.cluster import DBSCAN
import hdbscan
import numpy as np
import os
import shutil
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import pairwise_distances

class DBSCANClusterer():
    def __init__(self, input_image_dir, save_cluster_mapping_dir, eps = 0.20, use_pca=False):
        """
        input_image_dir: Directory containing images
        save_cluster_mapping_dir: Directory to save cluster mapping
        eps: Maximum distance between two samples for one to be considered as in the neighborhood of the other.
        use_pca: Whether to use PCA reduced embeddings or not
        """

        self.save_cluster_mapping_dir = save_cluster_mapping_dir
        if use_pca:
            print("Loading reduced embeddings")
            self.embeddings = np.load("embeddings/reduced_embeddings.npy")
        else:
            print("Loading original embeddings")
            self.embeddings = np.load("embeddings/embeddings.npy")
        self.input_image_dir = input_image_dir
        self.image_paths = [os.path.join(self.input_image_dir, i) for i in os.listdir(self.input_image_dir)]
        print("Loading DBSCAN")
        self.dbscan = DBSCAN(eps=eps, min_samples=5, metric='cosine')
        self.clusters = None
        self.cluster_to_images = None

    def fit_map_clusterer(self):
        """
        Fit the DBSCAN model and map the clusters to images in the input directory
        """

        self.dbscan.fit(self.embeddings)
        self.clusters = self.dbscan.labels_
        np.save(os.path.join(self.save_cluster_mapping_dir, 'clusters.npy'), self.clusters)
        #print(len(clusters))

        self.cluster_to_images = {}
        for label, img_path in zip(self.clusters, self.image_paths):    
            if label not in self.cluster_to_images:
                self.cluster_to_images[label] = set()
            self.cluster_to_images[label].add(os.path.basename(img_path))  

        # if -1 in self.cluster_to_images:
        #     del self.cluster_to_images[-1]
        
        #save cluster to images mapping
        print("Saving cluster to images mapping")
        np.save(os.path.join(self.save_cluster_mapping_dir, 'clustermapping.npy'), self.cluster_to_images)

    def save_clusters_to_folder(self, save_dir):
        """
        Save the clusters to folders for visual inspection
        """

        if self.cluster_to_images is None:
            self.cluster_to_images = np.load(os.path.join(self.save_cluster_mapping_dir, 'clustermapping.npy'), allow_pickle=True).item()
        if self.clusters is None:
            self.clusters = np.load(os.path.join(self.save_cluster_mapping_dir, 'clusters.npy'))
        print("Making cluster folders")
        for cluster, names in self.cluster_to_images.items():
            cluster_dir = os.path.join(save_dir, str(cluster))
            os.makedirs(cluster_dir, exist_ok=True)
            for name in names:
                shutil.copy(os.path.join(self.input_image_dir, name), cluster_dir)


class HDBSCANClusterer():
    def __init__(self, input_image_dir, save_cluster_mapping_dir, min_cluster_size=5, min_samples=5, use_pca=False):
        """
        input_image_dir: Directory containing images
        save_cluster_mapping_dir: Directory to save cluster mapping
        min_cluster_size: Minimum number of samples in a cluster
        min_samples: Number of samples in a neighborhood for a point to be considered as a core point
        use_pca: Whether to use PCA reduced embeddings or not
        """

        self.save_cluster_mapping_dir = save_cluster_mapping_dir
        if use_pca:
            print("Loading reduced embeddings")
            self.embeddings = np.load("embeddings/reduced_embeddings.npy")
        else:
            print("Loading original embeddings")
            self.embeddings = np.load("embeddings/embeddings.npy")
        self.input_image_dir = input_image_dir
        self.image_paths = [os.path.join(self.input_image_dir, i) for i in os.listdir(self.input_image_dir)]
        print("Loading HDBSCAN")
        self.hdbscan = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric="precomputed")
        self.clusters = None
        self.cluster_to_images = None

    def fit_map_clusterer(self):
        """
        Fit the HDBSCAN model and map the clusters to images in the input directory
        """

        print("Finding pairwise distances")
        distance_matrix = pairwise_distances(self.embeddings, metric='cosine')
        self.hdbscan.fit(distance_matrix.astype(np.float64))
        self.clusters = self.hdbscan.labels_
        np.save(os.path.join(self.save_cluster_mapping_dir, 'clusters.npy'), self.clusters)

        self.cluster_to_images = {}
        for label, img_path in zip(self.clusters, self.image_paths):
            if label not in self.cluster_to_images:
                self.cluster_to_images[label] = set()
            self.cluster_to_images[label].add(os.path.basename(img_path))

        print("Saving cluster to images mapping")
        np.save(os.path.join(self.save_cluster_mapping_dir, 'clustermapping.npy'), self.cluster_to_images)

    def save_clusters_to_folder(self, save_dir):
        """
        Save the clusters to folders for visual inspection
        """
        
        if self.cluster_to_images is None:
            self.cluster_to_images = np.load(os.path.join(self.save_cluster_mapping_dir, 'clustermapping.npy'), allow_pickle=True).item()
        if self.clusters is None:
            self.clusters = np.load(os.path.join(self.save_cluster_mapping_dir, 'clusters.npy'))
        print("Making cluster folders")
        for cluster, names in self.cluster_to_images.items():
            cluster_dir = os.path.join(save_dir, str(cluster))
            os.makedirs(cluster_dir, exist_ok=True)
            for name in names:
                shutil.copy(os.path.join(self.input_image_dir, name), cluster_dir)


# clus = DBSCANClusterer(r"data\faces", r"saved_cluster")
# #clus.split_cluster_by_similarity(1, 0.75)
# clus.save_clusters_to_folder(r'clusters')