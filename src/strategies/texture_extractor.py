# src/strategies/texture_extractor.py
from src.features import FeatureExtractor
from skimage import feature
import numpy as np

class TextureExtractor(FeatureExtractor):
    def extract(self, image):
        """Extrai descritores de textura usando LBP."""
        gray_image = image.convert('L')
        lbp = feature.local_binary_pattern(np.array(gray_image), P=24, R=3, method="uniform")
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 24 + 3), range=(0, 24 + 2))
        return hist / hist.sum()  # Normaliza o histograma
