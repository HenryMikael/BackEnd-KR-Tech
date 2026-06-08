import re
from functools import wraps
from flask import request, jsonify


# VALIDAÇÕES INDIVIDUAIS


def validar_email(email):
    """Valida formato de email"""
    if not email:
        return False
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))

def validar_senha(senha):
    """Valida força da senha (mínimo de 6 caracteres)"""
    if not senha:
        return False
    return len(senha) >= 6

def validar_preco(preco):
    """Valida se preço é positivo"""
    if preco is None:
        return False
    return isinstance(preco, (int, float)) and preco > 0

def validar_estoque(estoque):
    """Valida se estoque é não negativo"""
    if estoque is None:
        return False
    return isinstance(estoque, int) and estoque >= 0

def validar_nome(nome, min_len=2):
    """Valida se nome tem pelo menos min_len caracteres"""
    if not nome:
        return False
    return len(nome.strip()) >= min_len

def validar_quantidade(quantidade):
    """Valida quantidade positiva"""
    if quantidade is None:
        return False
    return isinstance(quantidade, int) and quantidade > 0

def validar_id(id):
    """Valida se ID é positivo"""
    return isinstance(id, int) and id > 0

def validar_endereco(endereco):
    """Valida se endereço não está vazio"""
    return endereco and len(endereco.strip()) >= 5

def validar_metodo_pagamento(metodo):
    """Valida método de pagamento"""
    metodos_validos = ['cartao_credito', 'cartao_debito', 'pix', 'boleto', 'paypal']
    return metodo in metodos_validos


# DECORATORS DE VALIDAÇÃO


def validar_json_requerido(campos_obrigatorios):
    """Decorator para validar campos obrigatórios no JSON"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type deve ser application/json'}), 400
            
            dados = request.get_json()
            if not dados:
                return jsonify({'error': 'JSON vazio ou inválido'}), 400
            
            campos_faltando = [campo for campo in campos_obrigatorios if campo not in dados]
            
            if campos_faltando:
                return jsonify({
                    'error': f'Campos obrigatórios faltando: {", ".join(campos_faltando)}'
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# FUNÇÕES DE RESPOSTA PADRONIZADA


def erro_campo_invalido(campo, motivo):
    """Retorna erro padronizado para campo inválido"""
    return jsonify({
        'error': f'Campo inválido: {campo}',
        'motivo': motivo
    }), 400

def erro_nao_encontrado(recurso, identificador=None):
    """Retorna erro padronizado para recurso não encontrado"""
    msg = f'{recurso} não encontrado'
    if identificador:
        msg = f'{recurso} com ID {identificador} não encontrado'
    return jsonify({'error': msg}), 404