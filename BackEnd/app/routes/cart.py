from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order
from models.order_item import OrderItem
from extensions import db
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from utils.validators import validar_json_requerido, validar_quantidade, erro_campo_invalido
from validators.cart_validators import validar_checkout

cart_bp = Blueprint('cart', __name__)

# ADICIONAR PRODUTO AO CARRINHO 
@cart_bp.route('/add', methods=['POST'])
@jwt_required()
@validar_json_requerido(['product_id'])
def add_to_cart():
    user_id = get_jwt_identity()
    dados = request.get_json()
    
    product_id = dados.get('product_id')
    quantidade = dados.get('quantidade', 1)
    
    if not validar_quantidade(quantidade):
        return erro_campo_invalido('quantidade', 'Quantidade deve ser maior que zero'), 400
    
    produto = Product.query.get(product_id)
    
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    if produto.estoque < quantidade:
        return jsonify({'error': 'Estoque insuficiente'}), 400
    
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    
    item_existente = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=produto.id
    ).first()

    if item_existente:
        item_existente.quantidade += quantidade
    else:
        novo_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantidade=quantidade
        )
        db.session.add(novo_item)

    db.session.commit()
    return jsonify({'message': 'Produto adicionado ao carrinho com sucesso'}), 200

#LISTAR CARRINHO
@cart_bp.route('', methods=['GET'])  # /api/cart
@jwt_required()
def list_cart():
    user_id = get_jwt_identity()
    
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart or not cart.itens:
        return jsonify({'itens': [], 'total': 0}), 200
    
    itens = []
    total = 0

    for item in cart.itens:
        subtotal = item.quantidade * item.produto.preco
        total += subtotal

        itens.append({
            'item_id': item.id,
            'produto': item.produto.nome,
            'preco': item.produto.preco,
            'quantidade': item.quantidade,
            'subtotal': subtotal
        })

    return jsonify({'itens': itens, 'total': total}), 200

#ALTERAR QUANTIDADE
@cart_bp.route('/item/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_quantity(item_id):

    dados = request.get_json()

    quantidade = dados.get('quantidade')

    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    if item.produto.estoque < quantidade:
        return jsonify({'error': 'Estoque insuficiente'}), 400
    
    item.quantidade = quantidade

    db.session.commit()

    return jsonify({'message': 'Quantidade atualizada'}), 200

#REMOVER ITEM 
@cart_bp.route('/item/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_item(item_id):
    
    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item removido do cart'}), 200

# CHECKOUT
@cart_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """Transforma o carrinho em pedido"""
    
    user_id = get_jwt_identity()
    dados = request.get_json()
    
    erro = validar_checkout(dados)
    if erro:
        return erro
    
    endereco_entrega = dados.get('endereco_entrega')
    metodo_pagamento = dados.get('metodo_pagamento')
    
    if not endereco_entrega:
        return jsonify({'error': 'Endereço de entrega é obrigatório'}), 400
    
    if not metodo_pagamento:
        return jsonify({'error': 'Método de pagamento é obrigatório'}), 400
    
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart or not cart.itens:
        return jsonify({'error': 'Carrinho vazio'}), 400
    
    for item in cart.itens:
        if item.produto.estoque < item.quantidade:
            return jsonify({
                'error': f'Estoque insuficiente para {item.produto.nome}. Disponível: {item.produto.estoque}'
            }), 400
    
    total = sum(item.quantidade * item.produto.preco for item in cart.itens)
    
    order = Order(
        user_id=user_id,
        total=total,
        endereco_entrega=endereco_entrega,
        metodo_pagamento=metodo_pagamento,
        status='pending'
    )
    db.session.add(order)
    db.session.flush()  # Para ter o order.id
    
    for item in cart.itens:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantidade=item.quantidade,
            preco_unitario=item.produto.preco
        )
        db.session.add(order_item)
        
        # Diminui o estoque
        item.produto.estoque -= item.quantidade
    
    CartItem.query.filter_by(cart_id=cart.id).delete()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Pedido realizado com sucesso!',
        'order_id': order.id,
        'total': total,
        'status': order.status
    }), 201