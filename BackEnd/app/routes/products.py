from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.decorators.admin_required import admin_required
from app.models.category import Category
from app.models.product  import Product
from app.utils.validators import validar_json_requerido, validar_id
from app.validators.product_validators import validar_produto
from extensions import db
import os

products_bp = Blueprint('products', __name__)

#CRIAR PRODUTO
@products_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validar_json_requerido(['nome', 'preco', 'categoria_id'])
def create_product():
    
    dados = request.get_json()

    nome = dados.get('nome')
    descricao = dados.get('descricao')
    preco = dados.get('preco')
    estoque = dados.get('estoque')
    categoria_id = dados.get('categoria_id')
    imagem_url = dados.get('imagem_url')

    erro = validar_produto(dados)
    if erro:
        return erro

    novo_produto = Product(
        nome=nome,
        descricao=descricao,
        preco=preco,
        estoque=estoque,
        categoria_id=categoria_id,
        imagem_url=imagem_url
    )

    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({'message': 'Produto criado com sucesso', 'id': novo_produto.id}), 201

#LISTAR PRODUTOS
@products_bp.route('/products', methods=['GET'])
def list_products():
    
    nome = request.args.get('nome')
    categoria = request.args.get('categoria') 

    query = Product.query

    if nome:
        query = query.filter(Product.nome.like(f'%{nome}%'))

    if categoria:
        query = query.join(Category).filter(Category.nome == categoria) 

    produtos = query.all()

    lista = []

    for produto in produtos:
        lista.append({
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'estoque': produto.estoque,
            'categoria': produto.categoria_rel.nome,
            'imagem_url': produto.imagem_url
        })

    return jsonify(lista), 200

#BUSCAR PRODUTO POR ID
@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):

    produto = Product.query.get(id)

    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify({
        'id': produto.id,
        'nome': produto.nome,
        'descricao': produto.descricao,
        'preco': produto.preco,
        'estoque': produto.estoque,
        'categoria': produto.categoria_rel.nome
    }), 200

#EDITAR PRODUTO
@products_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(id):

    dados = request.get_json()

    erro = validar_produto(dados, is_update=True)
    if erro:
        return erro
    
    produto = Product.query.get(id)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    produto.nome = dados.get('nome', produto.nome)
    produto.descricao = dados.get('descricao', produto.descricao)
    produto.preco = dados.get('preco', produto.preco)
    produto.estoque = dados.get('estoque', produto.estoque)
    produto.categoria_id = dados.get('categoria_id', produto.categoria_id)
    produto.imagem_url = dados.get('imagem_url', produto.imagem_url)

    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso'}), 200

#DELETAR PRODUTO
@products_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(id):

    produto = Product.query.get(id)

    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()
    

    return jsonify({'message': 'Produto deletado com sucesso'}), 200