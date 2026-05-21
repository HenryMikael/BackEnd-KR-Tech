from flask import Flask
from database import db

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

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/loja_virtual'
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(cart_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)