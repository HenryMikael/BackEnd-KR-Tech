from extensions import db

class CartItem(db.Model):
    __tablename__ = 'itens_carrinho'

    id = db.Column(db.Integer, primary_key=True)

    quantidade = db.Column(db.Integer, nullable=False, default=1)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey('carrinho.id'),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('produtos.id'),
        nullable=False
    )

    cart = db.relationship(
        'Cart',
        back_populates='itens'
    )