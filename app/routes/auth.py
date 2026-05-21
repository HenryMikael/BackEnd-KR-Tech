from flask import Blueprint, request, jsonify
from app.models.user import User
from database import db

auth_bp = Blueprint('auth', __name__)

#CADASTRO
@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json()

    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')

    if not nome or not senha or not email:
        return jsonify({'message': 'Preencha todos os campos'}), 400
    
    usuario_existente = User.query.filter_by(nome=nome).first()

    if usuario_existente:
        return jsonify({'message': 'Usuário já existe'}), 400
    
    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()
    

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

#LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()

    nome = dados.get('nome')
    senha = dados.get('senha')

    usuario = User.query.filter_by(nome=nome).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if not usuario.check_senha(senha):
        return jsonify({'error': 'Senha incorreta'}), 401
    
    return jsonify({'message': 'Login bem-sucedido',
                    'usuario': usuario.nome }), 200