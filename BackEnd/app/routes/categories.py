from flask import Blueprint, request, jsonify
from app.models.category import Category
from database import db

categories_bp = Blueprint('categories', __name__)

#CRIAR CATEGORIA
@categories_bp.route('/categories', methods=['POST'])
def create_category():

    dados = request.get_json()
    nome = dados.get('nome')
    if not nome:
        return jsonify({'error': 'Nome é obrigatório.'}), 400
    
    categoria_existente = Category.query.filter_by(nome=nome).first()

    if categoria_existente:
        return jsonify({'error': 'Categoria já existe.'}), 400
    
    nova_categoria = Category(nome=nome)

    db.session.add(nova_categoria)
    db.session.commit()
   

    return jsonify({'message': 'Categoria criada com sucesso.', 'categoria': {'id': nova_categoria.id, 'nome': nova_categoria.nome}}), 201

#LISTAR CATEGORIAS
@categories_bp.route('/categories', methods=['GET'])
def list_categories():

    categorias = Category.query.all()

    lista = []

    for categoria in categorias:
        lista.append({'id': categoria.id, 'nome': categoria.nome})

    return jsonify(lista), 200