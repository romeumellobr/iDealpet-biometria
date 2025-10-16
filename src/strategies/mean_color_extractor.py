import requests
import cv2
import numpy as np
from io import BytesIO

class MeanColorExtractor:
    def extract1(self, image_url):
        try:
            # Baixar a imagem da URL
            response = requests.get(image_url)
            if response.status_code != 200:
                raise ValueError(f"Erro ao baixar a imagem: status {response.status_code}")

            # Converte os dados da imagem para um array NumPy
            image = np.array(bytearray(response.content), dtype=np.uint8)
            
            # Decodifica a imagem para o formato adequado
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            
            # Verificar se a imagem foi carregada corretamente
            if image is None or image.size == 0:
                raise ValueError(f"Imagem não pôde ser carregada ou está vazia: {image_url}")
            
            # Calcular a média das cores (média sobre as dimensões 0 e 1)
            mean_color = np.mean(image, axis=(0, 1))  # Média das cores ao longo das linhas e colunas
            
            return mean_color
        
        except Exception as e:
            print(f"Erro ao extrair as características de cor: {e}")
            return None

    def extract(self, image):
        """
        Extrai a média de cor da imagem.

        Args:
            image (PIL.Image): Imagem a ser processada.

        Returns:
            np.array: Vetor de características de dimensão 128.
        """
        image_array = np.array(image)
        mean_colors = np.mean(image_array, axis=(0, 1))  # Vetor de dimensão (3,)

        # Redimensiona para 128 dimensões (repetindo valores ou interpolando)
        features = np.resize(mean_colors, 128)
        return features.tolist()
