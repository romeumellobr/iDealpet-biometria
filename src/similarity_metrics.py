# src/similarity_metrics.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EuclideanSimilarity:
    def compare(self, features1, features2):
        """
        Calcula a distância Euclidiana entre dois vetores de características.
        
        Args:
            features1 (list or np.array): Características da primeira imagem.
            features2 (list or np.array): Características da segunda imagem (do DB).
        
        Returns:
            float: Distância Euclidiana entre os vetores de características.
        """
        return np.linalg.norm(np.array(features1) - np.array(features2))


class CosineSimilarity:
    def compare(self, features1, features2):
        """
        Calcula a similaridade cosseno entre dois vetores de características.
        
        Args:
            features1 (list or np.array): Características da primeira imagem.
            features2 (list or np.array): Características da segunda imagem (do DB).
        
        Returns:
            float: Similaridade cosseno entre os vetores de características.
        """
        return cosine_similarity([features1], [features2])[0][0]