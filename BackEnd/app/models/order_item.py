from extensions import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'         

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)  # Congela o preço no momento da compra
    
    produto = db.relationship('Product', backref='order_itens')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'produto_nome': self.produto.nome if self.produto else None,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.quantidade * self.preco_unitario
        }