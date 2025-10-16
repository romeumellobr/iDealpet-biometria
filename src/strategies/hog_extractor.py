# src/strategies/hog_extractor.py
from skimage.feature import hog
from PIL import Image
import numpy as np
import cv2


class HOGExtractor:
    def extract(self, image):
        """
        Extrai características HOG (Histograma de Gradientes Orientados) da imagem.
        
        Args:
            image (PIL.Image): Imagem a ser processada.
        
        Returns:
            list: Vetor de características HOG.
        """
        # Converte a imagem para array de numpy em escala de cinza
        image_array = np.array(image.convert("L"))
        
        # Certifica-se de que a imagem tenha o tipo de dado correto
        image_array = np.uint8(image_array)  # Converte para o tipo esperado pelo OpenCV

        # Verifica se a imagem não está vazia
        if image_array.size == 0:
            raise ValueError("A imagem fornecida está vazia ou não foi carregada corretamente.")
        
        # Verifica se a imagem tem o formato esperado (2D, altura x largura)
        if len(image_array.shape) != 2:
            raise ValueError("A imagem precisa ser 2D (escala de cinza), mas foi recebida com forma {}".format(image_array.shape))
        
        # Inicializa o descritor HOG do OpenCV
        hog = cv2.HOGDescriptor()

        # Diagnóstico: Verificar se a imagem tem valores dentro do esperado
        print("Shape da imagem:", image_array.shape)
        print("Valores da imagem (exemplo):", image_array[0, :10])  # Apenas mostra os primeiros valores da primeira linha

        try:
            # Calcula os descritores HOG da imagem
            features = hog.compute(image_array)
        except Exception as e:
            raise ValueError(f"Erro ao calcular os descritores HOG: {e}")
        
        # Verifica se os descritores foram calculados corretamente
        if features is None or features.size == 0:
            raise ValueError("Falha ao calcular os descritores HOG. A imagem pode ser inadequada para este processo.")
        
        # Diagnóstico: Verificar as características extraídas
        print("Características HOG extraídas (exemplo):", features[:10])  # Mostra os primeiros 10 valores das características

        # Transforma o resultado em um vetor 1D
        features = features.flatten()  # Transforma o array de características em um vetor 1D
        
        return features.tolist()  # Retorna como lista


