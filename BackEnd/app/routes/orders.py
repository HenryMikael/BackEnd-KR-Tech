from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    user_id = get_jwt_identity()

    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify({
        'pedidos': [order.to_dict() for order in orders]
    }), 200

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()

    if not order:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    return jsonify(order.to_dict()), 200