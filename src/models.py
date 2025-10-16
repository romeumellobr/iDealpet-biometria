from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Boolean, ARRAY, DateTime, Date, func
from datetime import datetime
from pgvector.sqlalchemy import Vector

db = SQLAlchemy()

class Dog(db.Model):
    __tablename__ = "dogs"
    dog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID único do cão
    dog_name = db.Column(db.String(255), nullable=False)  # Nome do cão
    feature_vector = db.Column(db.ARRAY(db.Float), nullable=False)  # Vetor de características
    image_path = db.Column(db.String(255))  # Caminho da imagem do cão
    created_at = db.Column(db.DateTime, default=func.current_timestamp())  # Data de criação
    # Relacionamento com a tabela `features`
    features = db.relationship("Feature", backref="dog", cascade="all, delete-orphan")

class Feature(db.Model):
    __tablename__ = "features"
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.dog_id", ondelete="CASCADE"), nullable=False)
    descriptor_type = db.Column(db.String(50), nullable=False)  # Adicionando descriptor_type
    feature_vector = db.Column(Vector(128), nullable=False)  # pgvector para vetores
    created_at = db.Column(db.DateTime, default=func.current_timestamp())
    image_url = db.Column(db.String(255))
    
class Projetos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    fases = db.relationship("Fases", backref="projeto", lazy=True)

    def get_historico(self):
        return HistoricoDescricao.query.filter_by(entidade_tipo='projeto', entidade_id=self.id).all()


class Fases(db.Model):
    __tablename__ = 'fases'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    atividades = db.relationship('Atividades', backref='fases', lazy=True)
    descricao_historico = db.Column(db.Text, nullable=True)

class Atividades(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    fase_id = db.Column(db.Integer, db.ForeignKey('fases.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50), default='pendente')
    logs = db.relationship('Log', backref='atividades', lazy=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    descricao_historico = db.Column(db.Text, nullable=True)

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=True)
    mensagem = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  

class HistoricoDescricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidade_tipo = db.Column(db.String(50), nullable=False)  # 'projeto', 'fase' ou 'atividade'
    entidade_id = db.Column(db.Integer, nullable=False)
    descricao_anterior = db.Column(db.Text, nullable=False)
    nova_descricao = db.Column(db.Text, nullable=False)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("entidade_tipo IN ('projeto', 'fase', 'atividade')", name="check_entidade_tipo"),
    )