from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt

pca = PCA()
embeddings = np.load("embeddings/embeddings.npy")
reduced_embeddings = pca.fit(embeddings)
cumsum = np.cumsum(pca.explained_variance_ratio_)

plt.plot(cumsum)
plt.xlabel('Dimensions')
plt.ylabel('Explained Variance')
plt.title('PCA Explained Variance')
plt.show()

d = np.argmax(cumsum >= 0.95) + 1
print(f"Number of dimensions for 95% variance: {d}")
