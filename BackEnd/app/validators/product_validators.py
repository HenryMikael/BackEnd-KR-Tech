from app.utils.validators import (
    validar_nome, validar_preco, validar_estoque,
    erro_campo_invalido
)

def validar_produto(dados, is_update=False):
    """Valida dados de produto (criação ou atualização)"""

    if not is_update or dados.get('nome'):
        if not validar_nome(dados.get('nome'), min_length=3):
            return erro_campo_invalido('nome', 'Nome deve ter pelo menos 3 caracteres')
    
    if not is_update or dados.get('preco') is not None:
        if not validar_preco(dados.get('preco')):
            return erro_campo_invalido('preco', 'Preço deve ser maior que zero')
        
    if not is_update or dados.get('estoque') is not None:
        if not validar_estoque(dados.get('estoque')):
            return erro_campo_invalido('estoque', 'Estoque deve ser um número não negativo')
        
    if not is_update or dados.get('categoria_id'):
        if not dados.get('categoria_id'):
            return erro_campo_invalido('categoria_id', 'Categoria é obrigatória')

    return None