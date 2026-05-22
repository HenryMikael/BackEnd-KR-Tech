from flask import Blueprint, request, jsonify
from database import db

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product

cart_bp = Blueprint('cart', __name__)

#ADICIONAR PRODUTO AO CARRINHO
@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    dados = request.get_json()

    user_id = dados.get('user_id')
    product_id = dados.get('product_id')
    quantidade = dados.get('quantidade', 1)

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
        carrinho_id=cart.id,
        produto_id=product_id
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

    return jsonify({'message': 'Produto adicionado ao cart com sucesso'}), 200

#LISTAR cart
@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def list_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return jsonify({'error': 'cart vazio'}), 200
    
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

    return jsonify({
        'itens': itens,
        'total': total
    }), 200

#ALTERAR QUANTIDADE
@cart_bp.route('/cart/item/<int:item_id>', methods=['PUT'])
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
@cart_bp.route('/cart/item/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    item = CartItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item removido do cart'}), 200
