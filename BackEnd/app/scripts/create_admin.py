import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(BASE_DIR)

from main import app
from extensions import db
from app.models.user import User

def create_admin_user():
    """Cria um usuário admin padrão"""

    with app.app_context():
        admin_email = "kaeladmin@gmail.com"
        admin_nome = "Kael Admin"
        admin_senha = "admin@123"

        admin_existente = User.query.filter_by(email=admin_email).first()

        if admin_existente:
            print(f"Admin já existe: {admin_email}")

            if not admin_existente.is_admin:
                admin_existente.is_admin = True
                db.session.commit()
                print(f"✅ Usuário {admin_email} promovido a admin!")
            else:
                print(f"✅ {admin_email} já é admin")
            return
        
        novo_admin = User(
            nome=admin_nome,
            email=admin_email,
            is_admin=True,
            email_verificado=True
        )
        novo_admin.set_senha(admin_senha)

        db.session.add(novo_admin)
        db.session.commit()

if __name__ == "__main__":
    create_admin_user()