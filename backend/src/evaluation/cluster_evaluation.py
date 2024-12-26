from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

embeddings = np.load("embeddings/embeddings.npy")
clusters = np.load("saved_cluster/clusters.npy")

tsne = TSNE(n_components=3, random_state=0)
embeddings_3d = tsne.fit_transform(embeddings)

silhouette_avg = silhouette_score(embeddings, clusters)
print("Silhouette Score:", silhouette_avg)

db_index = davies_bouldin_score(embeddings, clusters)
print("Davies-Bouldin Index:", db_index)

ch_index = calinski_harabasz_score(embeddings, clusters)
print("Calinski-Harabasz Index:", ch_index)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(embeddings_3d[:, 0], embeddings_3d[:, 1], embeddings_3d[:, 2], c=clusters, cmap='Spectral')

plt.title('3D t-SNE Visualization of Clusters')
plt.colorbar(sc)
plt.show()
