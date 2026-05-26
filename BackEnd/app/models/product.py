from database import db

class Product(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    imagem_url = db.Column(db.Text)
        
    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey('categorias.id'),
        nullable=False
    )

    itens_carrinho = db.relationship(
        'CartItem',
        backref='produtos',
        lazy=True
    )