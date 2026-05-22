from flask import Blueprint, request, jsonify
from app.models.user import User
from database import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

#CADASTRO
@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json()

    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')
    type = dados.get('type')
    confirmar_senha = dados.get('confirmar_senha')

    if senha != confirmar_senha:
        return jsonify({'message': 'As senhas não coincidem'}), 400

    if not nome or not senha or not email:
        return jsonify({'message': 'Preencha todos os campos'}), 400
    
    usuario_existente = User.query.filter_by(nome=nome).first()

    if usuario_existente:
        return jsonify({'message': 'Usuário já existe'}), 400
    
    novo_usuario = User(nome=nome, email=email, type=type)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()
    

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

#LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()

    email = dados.get('email')
    senha = dados.get('senha')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if not usuario.check_senha(senha):
        return jsonify({'error': 'Senha incorreta'}), 401
    
    token = create_access_token(identity=usuario.id)
    
    return jsonify({
        'message': 'Login bem-sucedido',
        'token': token,                 # deixar apenas a mensagem de login bem-sucedido e o token, sem o id do usuário e o tipo
        'user_id': usuario.id,
        'type': usuario.type}), 200 

@auth_bp.route('/recover-password', methods=['PUT'])
def recover_password():

    dados = request.get_json()

    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    usuario.senha =  generate_password_hash(nova_senha)

    db.session.commit()

    return jsonify({'message': 'Senha atualizada com sucesso'}), 200