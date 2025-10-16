# src/features.py
from abc import ABC, abstractmethod

class FeatureExtractor(ABC):
    """Interface para extratores de features."""
    
    @abstractmethod
    def extract(self, image):
        """Método abstrato para extração de features."""
        pass
