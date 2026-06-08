# 🛒 E-commerce API

API RESTful para sistema de e-commerce desenvolvida em Flask.

## ✨ Funcionalidades

- Autenticação JWT
- Cadastro e login de usuários
- Verificação de email
- Recuperação de senha
- Carrinho de compras
- CRUD de produtos (admin)
- Sistema de categorias
- Painel administrativo

## 🚀 Tecnologias

- Python 3.11+
- Flask 2.3+
- SQLAlchemy
- JWT
- MySQL

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/HenryMikael/BackEnd-KR-Tech.git

# Entre na pasta
cd backend

# Crie ambiente virtual
python -m venv venv

# Ative o venv (Windows)
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# Edite o .env com suas configurações

# Execute
python main.py