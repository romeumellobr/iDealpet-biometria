# src/feature_extraction_manager.py
import requests
from PIL import Image
from io import BytesIO


from features import FeatureExtractor

class FeatureExtractionContext:
    def __init__(self, extractor: FeatureExtractor):
        self._extractor = extractor

    def set_extractor(self, extractor: FeatureExtractor):
        self._extractor = extractor

    def extract_features(self, image_url):
        return self._extractor.extract(image_url)


class FeatureExtractionManager:
    def __init__(self, strategies):
        """
        Inicializa o gerenciador com uma lista de estratégias de extração.
        
        Args:
            strategies (list): Lista de instâncias de extratores de features.
        """
        self.strategies = strategies

    def set_strategy(self, strategies):
            self.strategies = strategies  # Permite alternar a estratégia dinamicamente

    def extract_features(self, image_path):
        """
        Extrai e combina as features de acordo com as estratégias fornecidas.

        Args:
            image_path (str ou PIL.Image): URL, caminho local ou objeto PIL da imagem.

        Returns:
            list: Vetor combinado de features extraídas.
        """
        # Verifica se `image_path` é uma URL, caminho local, ou objeto `PIL.Image`
        if isinstance(image_path, str) and image_path.startswith("http"):
            # Caso seja uma URL, baixa e abre a imagem
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        elif isinstance(image_path, str):
            # Caso seja um caminho local, abre a imagem diretamente
            image = Image.open(image_path)
        elif isinstance(image_path, Image.Image):
            # Caso já seja um objeto PIL.Image, usa diretamente
            image = image_path
        else:
            raise ValueError("Invalid image_path provided. Must be a URL, local path, or PIL.Image object.")

        combined_features = []

        for strategy in self.strategies:
            # Extrai as features para cada estratégia
            features = strategy.extract(image)
            print(f"strategy: {strategy.name}")
            print(f"Características: {features}")  # Depuração
            # Confere se o retorno é uma lista (no caso de tolist)
            if isinstance(features, list):
                combined_features.extend(features)
            else:
                raise TypeError(f"Feature extraction failed: output from {strategy} is not a list.")

        return combined_features



        # Extrai as características usando as estratégias e combina os resultados
        #combined_features = []
        #for strategy in self.strategies:
            #features = strategy.extract(image)
            # Garante que `features` seja uma lista (caso seja um array numpy, converte com `.tolist()`)
            #combined_features.extend(features if isinstance(features, list) else features.tolist())

        #return image

    def extract_features1(self, image_path):
        """
        Extrai e combina as features de acordo com as estratégias fornecidas.
        
        Args:
            image_path (str): URL ou objeto PIL da imagem.
        
        Returns:
            list: Vetor combinado de features extraídas.
        """
        # Se image_path for uma URL (string começando com 'http')
        if isinstance(image_path, str) and image_path.startswith("http"):
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        elif isinstance(image_path, str):
            # Se for um caminho local, abre a imagem
            image = Image.open(image_path)
        elif isinstance(image_path, Image.Image):
            # Se for um objeto PIL.Image já, usa diretamente
            image = image_path
        else:
            raise ValueError("Invalid image_path provided. Must be a URL, local path, or PIL.Image object.")

        # Extrair as características
        combined_features = []
        for strategy in self.strategies:
            features = strategy.extract(image)
            combined_features.extend(features if isinstance(features, list) else features.tolist())
        
        return combined_features

    def extract_features3(self, image_path, combined=True):
        """
        Extrai features da imagem de acordo com as estratégias fornecidas.
        
        Args:
            image_path (str): URL ou caminho local da imagem.
            combined (bool): Se True, retorna um vetor combinado; 
                             se False, retorna um dicionário com features por nome de estratégia.
        
        Returns:
            list ou dict: Vetor combinado de features ou dicionário de features por estratégia.
        """
        # Carrega a imagem, seja de URL ou do caminho local
        if image_path.startswith("http"):
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_path)

        if combined:
            # Combina todas as features em um único vetor
            combined_features = []
            for strategy in self.strategies:
                features = strategy.extract(image)
                combined_features.extend(features if isinstance(features, list) else features.tolist())
            return combined_features
        else:
            # Retorna as features em um dicionário separado por estratégia
            features_dict = {}
            for strategy in self.strategies:
                feature_name = strategy.__class__.__name__.lower()  # Nome da estratégia em minúsculas
                features = strategy.extract(image)
                features_dict[feature_name] = features if isinstance(features, list) else features.tolist()
            return features_dict

    def extract_features2(self, image_url):
        """
        Extrai e combina as features de acordo com as estratégias fornecidas.
        
        Args:
            image_path (str): Caminho da imagem.
        
        Returns:
            list: Vetor combinado de features extraídas.
        """
        image = Image.open(image_url)
        combined_features = []

        for strategy in self.strategies:
            features = strategy.extract(image)
            # Converte para lista e concatena ao vetor combinado
            combined_features.extend(features if isinstance(features, list) else features.tolist())
        
        return combined_features

    def extract_features4(self, image_url):
        """
        Extrai as features da imagem usando as estratégias fornecidas.
        :param image_url: URL da imagem a ser processada.
        :return: Um dicionário contendo as features extraídas de todas as estratégias.
        """
        features = {}

        # Itera sobre as estratégias e extrai as características
        for strategy in self.strategies:
            feature_name = strategy.__class__.__name__.lower()  # Nome da estratégia em minúsculas
            features[feature_name] = strategy.extract(image_url)

        return features