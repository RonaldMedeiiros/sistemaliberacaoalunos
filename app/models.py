from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    ra = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    foto = db.Column(db.LargeBinary)  # Armazena o arquivo da foto em bytes
    matricula = db.Column(db.String(50))
    turno = db.Column(db.String(20))
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())