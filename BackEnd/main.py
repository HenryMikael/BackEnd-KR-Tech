from flask import Flask
from database import db
from flask_cors import CORS
from app.extensions import mail
import os

#UPLOADS
UPLOAD_FOLDER = 'uploads/products'

#MODELS
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.cart import Cart
from app.models.cart_item import CartItem

#ROTAS
from app.routes.auth import auth_bp
from app.routes.products import products_bp
from app.routes.categories import categories_bp
from app.routes.cart import cart_bp

#CONFIGURAÇÕES DO FLASK
app = Flask(__name__)
CORS(app)

# CONFIGURAÇÕES DO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/loja_virtual'

#CONFIGURAÇÕES DE E-MAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']  = 'krtechstorebr@gmail.com'
app.config['MAIL_PASSWORD']  = 'idak lent hkha tjdd'

#CONFIGURAÇÕES DE UPLOAD
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#INICIALIZAÇÃO DAS EXTENSÕES
db.init_app(app)
mail.init_app(app)

#REGISTRANDO AS BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)