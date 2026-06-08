from extensions import db

class Category(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    produtos = db.relationship(
        'Product',
        backref='categoria_rel',
        lazy=True
    )