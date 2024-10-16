from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from PIL import Image
import torch
import numpy as np
import os
from sklearn.decomposition import PCA

# FACE_DIR = r"data\faces"
# EMBEDDING_SAVE_DIR = r"embeddings"

class EmbeddingGenerator():
    def __init__(self, n_components = 50, use_pca=False, pca_save_dir=None):
        print("Embedding generator initializing")
        self.embedding_model = InceptionResnetV1(pretrained='vggface2').eval()
        print("Embedding model initialized successfully")
        print("Transforms initializing")
        self.transform = transforms.Compose([transforms.Resize((160, 160)), transforms.ToTensor()])

        self.use_pca = use_pca
        self.pca = PCA(n_components=n_components) if use_pca else None
        self.pca_save_dir = pca_save_dir
        if use_pca and pca_save_dir:
            self.load_pca_model(pca_save_dir)

    def create_and_save_embeddings(self, face_dir, embedding_save_dir):
        images = [os.path.join(face_dir, f) for f in os.listdir(face_dir) if f.endswith(('jpg'))]

        embeddings = []

        for image in images:
            print(f"Generating embedding for {os.path.basename(image)}")
            img = Image.open(image)
            img = self.transform(img)
            img = img.unsqueeze(0)
            with torch.no_grad():
                embedding = self.embedding_model(img)
            
            embeddings.append(embedding.cpu().numpy())

        embeddings = np.vstack(embeddings)

        if self.use_pca:
            print("Fitting PCA on embeddings")
            reduced_embeddings = self.pca.fit_transform(embeddings)
            np.save(os.path.join(embedding_save_dir, "reduced_embeddings.npy"), reduced_embeddings)

            if self.pca_save_dir:
                self.save_pca_model(self.pca_save_dir)
        
        np.save(os.path.join(embedding_save_dir, "embeddings.npy"), embeddings)


    def inference_embedding(self, image_path):
        '''
        Gives the embedding for a single image during inference

        Args:
            image_path: path of image
        
        Returns:
            embeddings
        '''
        img = Image.open(image_path)
        img = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            embedding = self.embedding_model(img).cpu().numpy()

        if self.use_pca:
            print("Applying PCA to embedding during inference")
            embedding = self.pca.transform(embedding)

        return embedding
    
    def save_pca_model(self, pca_save_dir):
        np.save(os.path.join(pca_save_dir, "pca_components.npy"), self.pca.components_)
        np.save(os.path.join(pca_save_dir, "pca_mean.npy"), self.pca.mean_)
        np.save(os.path.join(pca_save_dir, "pca_variance.npy"), self.pca.explained_variance_)

    def load_pca_model(self, pca_save_dir):
        if os.path.exists(os.path.join(pca_save_dir, "pca_components.npy")):
            print("Loading saved PCA model")
            self.pca.components_ = np.load(os.path.join(pca_save_dir, "pca_components.npy"))
            self.pca.mean_ = np.load(os.path.join(pca_save_dir, "pca_mean.npy"))
            self.pca.explained_variance_ = np.load(os.path.join(pca_save_dir, "pca_variance.npy"))
        else:
            print("No saved PCA model found")

    def apply_pca_on_exising_embeddings(self, embeddings_path, pca_save_dir, embedding_save_dir):
        embeddings = np.load(embeddings_path)
        reduced_embeddings = self.pca.fit_transform(embeddings)
        np.save(os.path.join(embedding_save_dir, "reduced_embeddings.npy"), reduced_embeddings)
        print("PCA applied on existing embeddings")
        self.save_pca_model(pca_save_dir)