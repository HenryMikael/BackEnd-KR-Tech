from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    codigo_ativacao = db.Column(db.String(6))
    codigo_recuperacao = db.Column(db.String(6))
    email_verificado = db.Column(db.Boolean, default=False)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)

    carrinhos = db.relationship(
    'Cart',
    backref='usuario',
    lazy=True
)