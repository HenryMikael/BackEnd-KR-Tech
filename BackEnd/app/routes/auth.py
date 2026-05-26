from flask import Blueprint, request, jsonify
from app.models.user import User
from database import db
from werkzeug.security import generate_password_hash
import random
from app.services.email_service import send_email

auth_bp = Blueprint('auth', __name__)

#CADASTRO
@auth_bp.route('/register', methods=['POST'])
def register():
    dados = request.get_json()

    nome = dados.get('nome')
    senha = dados.get('senha')
    email = dados.get('email')
    confirmar_senha = dados.get('confirmar_senha')

    codigo = str(random.randint(100000, 999999))

    if senha != confirmar_senha:
        return jsonify({'message': 'As senhas não coincidem'}), 400

    if not nome or not senha or not email:
        return jsonify({'message': 'Preencha todos os campos'}), 400
    
    usuario_existente = User.query.filter_by(nome=nome).first()

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

    return jsonify({'message': 'codigo enviado para o email'}), 201

#LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()

    email = dados.get('email')
    senha = dados.get('senha')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    if not usuario.email_verificado:
        return jsonify({'error': 'Email não verificado'}), 401

    if not usuario.check_senha(senha):
        return jsonify({'error': 'Senha incorreta'}), 401
    
    return jsonify({
        'message': 'Login bem-sucedido'
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
    nova_senha = dados.get('nova_senha')

    usuario = User.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({
            'erro': 'Usuário não encontrado'
        }), 404

    usuario.senha = generate_password_hash(nova_senha)

    usuario.codigo_recuperacao = None

    db.session.commit()

    return jsonify({
        'mensagem': 'Senha alterada com sucesso'
    })