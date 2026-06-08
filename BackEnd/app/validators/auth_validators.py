from utils.validators import (
    validar_email, validar_senha, validar_nome,
    erro_campo_invalido
    )

def validar_registro(dados):
    """Valida dados de registro de usuário"""

    #validar nome
    if not validar_nome(dados.get('nome')):
        return erro_campo_invalido('nome', 'Nome deve ter pelo menos 2 caracteres')
    
    #validar email
    if not validar_email(dados.get('email')):
        return erro_campo_invalido('email', 'Email inválido')
    
    #valida senha
    if not validar_senha(dados.get('senha')):
        return erro_campo_invalido('senha', 'Senha deve ter pelo menos 6 caracteres')

    #valida confirmação de senha
    if dados.get('senha') != dados.get('confirmar_senha'):
        return erro_campo_invalido('confirmar_senha', 'As senhas não coincidem')

    return None

def validar_login(dados):
    """Valida dados de login"""

    if not dados.get('email'):
        return erro_campo_invalido('email', 'Email é obrigatório')
    
    if not validar_email(dados.get('email')):
        return erro_campo_invalido('email', 'Email inválido')
    
    if not dados.get('senha'):
        return erro_campo_invalido('senha', 'Senha é obrigatória')
    
    return None