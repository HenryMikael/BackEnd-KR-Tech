from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    endereco_entrega = db.Column(db.String(500), nullable=False)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = db.relationship('usuarios', backref=db.backref('orders', lazy=True))
    itens = db.relationship('OrderItem', backref='order', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'status': self.status,
            'endereco_entrega': self.endereco_entrega,
            'metodo_pagamento': self.metodo_pagamento,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'itens': [item.to_dict() for item in self.itens]
        }