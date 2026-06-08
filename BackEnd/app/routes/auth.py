from flask import Blueprint, request, jsonify
from app.models.user import User
from extensions import db
import random
from services.email_service import send_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.validators import validar_json_requerido
from validators.auth_validators import validar_registro, validar_login

auth_bp = Blueprint('auth', __name__)

#CADASTRO
@auth_bp.route('/register', methods=['POST'])
@validar_json_requerido(['nome', 'email', 'senha', 'confirmar_senha'])
def register():
    dados = request.get_json()
    
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    
    erro = validar_registro(dados)
    if erro:
        return erro
    
    codigo = str(random.randint(100000, 999999))
    
    usuario_existente = User.query.filter_by(email=email).first()
    
    if usuario_existente:
        return jsonify({'message': 'Usuário já existe'}), 400
    
    novo_usuario = User(
        nome=nome,
        email=email,
        codigo_ativacao=codigo,
        email_verificado=False
    )
    novo_usuario.set_senha(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    send_email(email, codigo)
    
    return jsonify({'message': 'Código enviado para o email'}), 201

#LOGIN
@auth_bp.route('/login', methods=['POST'])
@validar_json_requerido(['email', 'senha'])
def login():
    dados = request.get_json()
    
    email = dados.get('email')
    senha = dados.get('senha')
    
    erro = validar_login(dados)
    if erro:
        return erro
    
    usuario = User.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if not usuario.email_verificado:
        return jsonify({'error': 'Email não verificado'}), 401
    
    if not usuario.verificar_senha(senha):
        return jsonify({'error': 'Senha incorreta'}), 401
    
    access_token = create_access_token(identity=usuario.id)
    
    return jsonify({
        'message': 'Login bem-sucedido',
        'access_token': access_token,
        'user_id': usuario.id,          
        'nome': usuario.nome 
    }), 200

#RECUPERAR SENHA
@auth_bp.route('/recover-password', methods=['PUT'])
def recover_password():

    dados = request.get_json()

    email = dados.get('email')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    codigo = str(random.randint(100000, 999999))
    usuario.codigo_recuperacao = codigo

    db.session.commit()

    send_email(email, codigo)

    return jsonify({'message': 'Codigo enviado com sucesso'}), 200

#VERIFICAR EMAIL
@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    dados = request.get_json()

    email = dados.get('email')
    codigo = dados.get('codigo')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if str(usuario.codigo_ativacao).strip() != str(codigo):
        return jsonify({'error': 'Código de ativação inválido'}), 400
    
    usuario.email_verificado = True
    usuario.codigo_ativacao = None

    db.session.commit()

    return jsonify({'message': 'Email verificado com sucesso'}), 200

@auth_bp.route('/verify-recover-code', methods=['POST'])
def verify_recover_code():
    dados = request.get_json()

    email = dados.get('email')
    codigo = dados.get('codigo')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    if usuario.codigo_recuperacao != codigo:
        return jsonify({'error': 'Código de recuperação inválido'}), 400
    
    return jsonify({'message': 'Código de recuperação verificado com sucesso'}), 200

@auth_bp.route('/reset-password', methods=['POST']) 
def reset_password(): 
    dados = request.get_json()

    email = dados.get('email') 
    codigo = dados.get('codigo') 
    nova_senha = dados.get('nova_senha') 

    if not email or not codigo or not nova_senha: 
        return jsonify({ 'error': 'Preencha todos os campos' }), 400
    
    usuario = User.query.filter_by(email=email).first() 

    if not usuario: 
        return jsonify({ 'error': 'Usuário não encontrado' }), 404 
    
    if str(usuario.codigo_recuperacao).strip() != str(codigo).strip(): 
        return jsonify({ 'error': 'Código inválido' }), 400 
    
    usuario.set_senha(nova_senha) 
    usuario.codigo_recuperacao = None 

    db.session.commit() 

    return jsonify({ 'message': 'Senha alterada com sucesso' }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    usuario = User.query.get(user_id)

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'email': usuario.email,
        'email_verificado': usuario.email_verificado
    }), 200

@auth_bp.route('/logout', methods=['POST']) 
@jwt_required()
def logout(): 
    usuario_id = get_jwt_identity() 
    return jsonify({ 
        'message': 'Logout realizado com sucesso', 
        'user_id': usuario_id 
    }), 200
