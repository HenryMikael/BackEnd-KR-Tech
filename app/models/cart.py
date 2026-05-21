from database import db

class Cart(db.Model):
    __tablename__ = 'carrinho'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )

    itens = db.relationship(
        'CartItem',
        back_populates='cart',
        cascade='all, delete-orphan'
    )