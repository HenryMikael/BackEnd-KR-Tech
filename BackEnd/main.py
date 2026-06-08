from flask import Flask
from config import Config
from extensions import db, jwt, mail, cors

#ROTAS
from app.routes.products import products_bp
from app.routes.categories import categories_bp
from app.routes.auth import auth_bp
from app.routes.cart import cart_bp
from app.routes.orders import orders_bp

#CONFIGURAÇÕES DO FLASK
app = Flask(__name__)
app.config.from_object(Config)

#INICIALIZAÇÃO DAS EXTENSÕES
db.init_app(app)
mail.init_app(app)
jwt.init_app(app)
cors.init_app(app)

#REGISTRANDO AS BLUEPRINTS
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(cart_bp, url_prefix='/api/cart')
app.register_blueprint(orders_bp, url_prefix='/api/orders')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)