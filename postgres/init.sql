-- Create the 'store' database
CREATE DATABASE dogs;

-- Habilita a extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Cria a tabela para armazenar os descritores
CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,
    dog_id INT REFERENCES dogs(dog_id),
    descriptor_type VARCHAR(50),
    feature_vector vector(128), -- Ajuste para o tamanho do seu vetor
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria um índice para acelerar buscas vetoriais (opcional)
CREATE INDEX features_vector_idx ON features USING ivfflat (feature_vector);
