# src/strategies/sift_extractor.py
import cv2
import numpy as np
import requests

from src.features import FeatureExtractor
from sklearn.metrics.pairwise import cosine_similarity

from io import BytesIO
from PIL import Image

class SIFTExtractor:
    """
    Classe responsável por extrair características SIFT de uma imagem fornecida.
    """
    def __init__(self):
        self.name = "SIFT"

    def extract(self, image_input):
        """
        Extrai características SIFT de uma imagem fornecida via URL ou objeto PIL.Image.

        Args:
            image_input (str ou PIL.Image): URL da imagem ou objeto PIL.Image.

        Returns:
            list: Vetor unidimensional das características SIFT extraídas.

        Raises:
            RuntimeError: Em caso de falha na extração ou processamento da imagem.
        """
        try:
            # Determinar se a entrada é uma URL ou um objeto PIL.Image
            if isinstance(image_input, str):
                # Fazer o download da imagem a partir da URL
                response = requests.get(image_input)
                if response.status_code != 200:
                    raise ValueError(f"Erro ao baixar a imagem. Código de status: {response.status_code}")

                # Decodificar a imagem para um array OpenCV
                image_array = np.frombuffer(response.content, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            elif isinstance(image_input, Image.Image):
                # Converter o objeto PIL.Image em um array OpenCV
                image = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)

            else:
                raise ValueError("Entrada inválida. Forneça uma URL ou um objeto PIL.Image.")

            # Verificar se a imagem foi carregada corretamente
            if image is None:
                raise ValueError("Erro ao carregar a imagem. A imagem pode estar corrompida ou o URL é inválido.")

            # Converter a imagem para escala de cinza
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Inicializar o SIFT
            sift = cv2.SIFT_create()

            # Detectar keypoints e calcular descritores
            keypoints, descriptors = sift.detectAndCompute(gray_image, None)

            # Verificar se os descritores foram gerados
            if descriptors is None or len(descriptors) == 0:
                raise ValueError("Nenhum descritor SIFT encontrado na imagem.")

            if descriptors is not None:
                # Calcula a média dos descritores para gerar um vetor fixo
                feature_vector = descriptors.mean(axis=0)
                return feature_vector.tolist()
            else:
                raise ValueError("No descriptors found.")


            # Retornar os descritores como uma lista unidimensional
            #return descriptors.flatten().tolist()

        except Exception as e:
            # Lançar um erro detalhado caso algo falhe
            raise RuntimeError(f"Falha na extração das características SIFT: {str(e)}")

class SIFTExtractor2(FeatureExtractor):
    def extract1(self, image_url):
        # Carregar a imagem a partir da URL
        image_data = requests.get(image_url).content
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Inicializar o SIFT detector
        sift = cv2.SIFT_create()
        
        # Detectar keypoints e descritores
        keypoints, descriptors = sift.detectAndCompute(image, None)
        
        if descriptors is not None and len(descriptors) > 0:
            # Vamos garantir que estamos pegando apenas o primeiro vetor de características
            return {"sift": descriptors[0].tolist()}  # Converte o descritor para lista
        else:
            # Se não encontrar descritores, retornamos um vetor vazio
            print("Aviso: Nenhum descritor SIFT encontrado.")
            return {"sift": []}

    def extract(self, image_url):
        try:
          image = self.load_image_from_url(image_url)
          print(f"Imagem carregada: {image.shape}")
          sift = cv2.SIFT_create()
          keypoints, descriptors = sift.detectAndCompute(image, None)
          if descriptors is not None:
            return {"sift": descriptors}
          else:
            raise ValueError("Descritores SIFT não encontrados.")
        except Exception as e:
          print(f"Erro ao extrair características SIFT: {e}")
          return {"error": str(e)}


