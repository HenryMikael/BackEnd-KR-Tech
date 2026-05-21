from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.models.product  import Product
from app.models.user import User
from database import db

products_bp = Blueprint('products', __name__)

#CRIAR PRODUTO
@products_bp.route('/products', methods=['POST'])
def create_product():

    dados = request.get_json()

    user_id = dados.get('user_id')

    usuario = User.query.get(user_id)

    #VERIFICAÇÃO DE ADMIN
    if not usuario or usuario.type != 'admin':
        return jsonify({'error': 'Apenas admins podem criar produtos'}), 403

    nome = dados.get('nome')
    descricao = dados.get('descricao')
    preco = dados.get('preco')
    estoque = dados.get('estoque')
    categoria_id = dados.get('categoria_id')

    if not nome or not descricao or preco is None or not categoria_id:
        return jsonify({'error': 'Preencha todos os campos'}), 400

    categoria = Category.query.get(categoria_id)

    if not categoria:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    novo_produto = Product(
        nome=nome,
        descricao=descricao,
        preco=preco,
        estoque=estoque,
        categoria_id=categoria_id
    )

    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({'message': 'Produto criado com sucesso'}), 201

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
            'categoria': produto.categoria_rel.nome
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
        'categoria': produto.categoria
    }), 200

#EDITAR PRODUTO
@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):

    produto = Product.query.get(id)

    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    produto.nome = request.json.get('nome', produto.nome)
    produto.descricao = request.json.get('descricao', produto.descricao)
    produto.preco = request.json.get('preco', produto.preco)
    produto.estoque = request.json.get('estoque', produto.estoque)
    produto.categoria = request.json.get('categoria', produto.categoria)

    db.session.commit()
    

    return jsonify({'message': 'Produto atualizado com sucesso'}), 200

#DELETAR PRODUTO
@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):

    produto = Product.query.get(id)

    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()
    

    return jsonify({'message': 'Produto deletado com sucesso'}), 200