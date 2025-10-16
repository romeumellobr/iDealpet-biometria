# src/strategies/keypoints_extractor.py
from src.features import FeatureExtractor
import cv2
import numpy as np

class KeypointsExtractor(FeatureExtractor):
    def extract(self, image):
        """Extrai keypoints e seus descritores usando SIFT."""
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray_image, None)
        return descriptors  # Retorna os descritores dos keypoints
		