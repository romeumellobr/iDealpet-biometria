from flask import Flask, render_template, jsonify, request
import logging
import os
from flasgger import Swagger, swag_from
import sys
from config import Config
from models import db, Dog
from database import DB
from config import config
from flask_migrate import Migrate
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from strategies.sift_extractor import SIFTExtractor
from similarity_metrics import EuclideanSimilarity, CosineSimilarity
from feature_extraction_manager import FeatureExtractionManager
from datetime import datetime

# Configura o logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = "sua_chave_secreta"

# Configuração do Swagger
swagger = Swagger(app)

migrate = Migrate(app, db)

db.init_app(app)

database = DB(config)

#  Default - Rota de abertura - tela principal - lista Cães cadastrados
@app.route("/")
def index():
    try:
        dogs = database.fetch_dogs_from_database()  
        if dogs:
            return render_template('index.html', dogs=dogs)
        else:
            return render_template('error.html', error="Nenhum registro encontrado na tabela 'dogs'.")
    except Exception as e:
        return render_template('error.html', error=str(e))

#
#  Versao 1 
#
@app.route('/v1/add_dog', methods=['POST'])
@swag_from('biometria.yml')
def add_dog_v1():
    try:
        data = request.json
        image_url = data.get("image_url")
        dog_name = data.get('dog_name')
        
        if not image_url:
            return jsonify({"error": "URL da imagem não fornecida"}), 400

        # Inicializar o FeatureExtractionManager com a estratégia SIFT
        manager = FeatureExtractionManager([SIFTExtractor()])

        # Extração das características
        feature_vector = manager.extract_features(image_url)
        
        if not feature_vector:
            return jsonify({"error": "Falha ao extrair características"}), 500

        # Inserir no banco de dados
        dog_id = database.insert_dog(dog_name, feature_vector, image_url)
        
        return jsonify({"message": "Cão e informações biomêtricas inseridas com sucesso", "dog_id": dog_id, "dog_name": dog_name}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v1/identify_dog', methods=['POST'])
@swag_from('biometria.yml')
def identify_dog_v1():
    # Recebe a URL da imagem e a métrica de similaridade
    image_url = request.json.get('image_url')
    
    similarity_metric_name = request.json.get('similarity_metric', 'cosine')

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    # Confere se a métrica fornecida é válida
    if similarity_metric_name not in similarity_metrics:
        return jsonify({"error": f"Invalid similarity metric: '{similarity_metric_name}'. Available metrics: {list(similarity_metrics.keys())}"}), 400

    # Seleciona a métrica de similaridade
    similarity_metric = similarity_metrics[similarity_metric_name]

    # Seleciona o extrator de características (usando SIFT no exemplo)
    feature_extractor = SIFTExtractor()

    # Cria o gerenciador de extração de características
    extractor = FeatureExtractionManager(strategies=[feature_extractor])

    try:
        # Extrai as características da imagem fornecida
        provided_image_features = extractor.extract_features(image_url)

        # Recupera as características dos cachorros no banco de dados
        saved_features_list = database.get_saved_features()  # Função que retorna as características salvas

        closest_dog = None
        closest_score = float('inf')  # Para comparação, menor distância significa maior similaridade

        # Compara a imagem fornecida com as imagens salvas no banco de dados
        for saved_dog_id, saved_features in saved_features_list:
            # Garante que os vetores de características sejam compatíveis (convertendo em arrays 2D para o cálculo de similaridade)
            provided_features_array = np.array(provided_image_features).reshape(1, -1)  # Redimensiona para um vetor 2D
            saved_features_array = np.array(saved_features).reshape(1, -1)  # Redimensiona para um vetor 2D

            # Calcula a similaridade entre as características usando a métrica de similaridade escolhida
            similarity_score = similarity_metric(provided_features_array, saved_features_array)[0][0]

            # Atualiza o cachorro mais próximo
            if similarity_score < closest_score:  # Quanto menor o valor, maior a similaridade no caso do cosine
                closest_score = similarity_score
                closest_dog = saved_dog_id

        # Se encontrar um cachorro correspondente, retorna o ID e a pontuação de similaridade
        if closest_dog:
            return jsonify({"dog_id": closest_dog, "similarity_score": closest_score}), 200
        else:
            return jsonify({"message": "No matching dog found"}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to extract features: {str(e)}"}), 500

#  Versao 2 
#

similarity_metrics = {
    "cosine": cosine_similarity
}

@app.route('/v2/add_dog', methods=['POST'])
def add_dog_v2():
    try:
        data = request.json
        image_url = data.get("image_url")
        dog_name = data.get('dog_name')
        
        if not image_url:
            return jsonify({"error": "URL da imagem não fornecida"}), 400

        # Inicializar o FeatureExtractionManager com a estratégia SIFT
        
        manager = FeatureExtractionManager([SIFTExtractor()])

        # Extração das características
        feature_vector = manager.extract_features(image_url)
        if not feature_vector:
            return jsonify({"error": "Falha ao extrair características"}), 500

        # Inserir no banco de dados
        dog_id = database.insert_dog(dog_name, feature_vector, image_url)
        return jsonify({"message": "Cão e informações biomêtricas inseridas com sucesso", "dog_id": dog_id, "dog_name": dog_name}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/v2/identify_dog', methods=['POST'])
def compare_dog_features_v2():
    """
    Compara características da imagem fornecida com características salvas no banco de dados.
    Calcula a distância Euclidiana e a similaridade do cosseno.
    """
    # Recebe a URL da imagem
    image_url = request.json.get('image_url')

    if not image_url:
        return jsonify({"error": "image_url is required"}), 400

    # Seleciona o extrator de características (usando SIFT no exemplo)
    feature_extractor = SIFTExtractor()

    # Cria o gerenciador de extração de características
    extractor = FeatureExtractionManager(strategies=[feature_extractor])

    try:
        # Extrai as características da imagem fornecida
        provided_image_features = extractor.extract_features(image_url)

        # Recupera as características dos cachorros no banco de dados
        saved_features_list = database.get_saved_features()  # Função que retorna as características salvas

        # Inicializa variáveis para rastrear o cachorro mais próximo
        closest_dog_euclidean = None
        closest_dog_cosine = None
        closest_score_euclidean = float('inf')  # Para distância Euclidiana, menor é melhor
        closest_score_cosine = -1.0  # Para similaridade do cosseno, maior é melhor

        # Compara a imagem fornecida com as imagens salvas no banco de dados
        for saved_dog_id, saved_features in saved_features_list:
            # Converte os vetores de características em arrays numpy
            provided_features_array = np.array(provided_image_features).flatten()
            saved_features_array = np.array(saved_features).flatten()

            # Calcula a distância Euclidiana
            euclidean_distance = np.linalg.norm(provided_features_array - saved_features_array)
            if euclidean_distance < closest_score_euclidean:
                closest_score_euclidean = euclidean_distance
                closest_dog_euclidean = saved_dog_id

            # Calcula a similaridade do cosseno
            cosine_similarity = np.dot(provided_features_array, saved_features_array) / (
                np.linalg.norm(provided_features_array) * np.linalg.norm(saved_features_array)
            )
            if cosine_similarity > closest_score_cosine:
                closest_score_cosine = cosine_similarity
                closest_dog_cosine = saved_dog_id

        # Retorna os resultados
        return jsonify({
            "euclidean": {
                "dog_id": closest_dog_euclidean,
                "distance": closest_score_euclidean
            },
            "cosine": {
                "dog_id": closest_dog_cosine,
                "similarity": closest_score_cosine
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to extract features: {str(e)}"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080,debug=True)   