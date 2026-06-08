from utils.validators import validar_quantidade, erro_campo_invalido

def validar_checkout(dados):
    """Valida dados de checkout"""

    if not dados.get('endereco_entrega'):
        return erro_campo_invalido('endereco_entrega', 'Endereço de entrega é obrigatório')
    
    if len(dados.get('endereco_entrega', '').strip()) < 5:
        return erro_campo_invalido('endereco_entrega', 'Endereço muito curto')
    
    if not dados.get('metodo_pagamento'):
        return erro_campo_invalido('metodo_pagamento', 'Método de pagamento é obrigatório')
    
    metodos_validos = ['cartao_credito', 'cartao_debito', 'pix', 'boleto']
    if dados.get('metodo_pagamento') not in metodos_validos:
        return erro_campo_invalido('metodo_pagamento', 
                                   f'Método inválido. Opções: {", ".join(metodos_validos)}')
    
    return None