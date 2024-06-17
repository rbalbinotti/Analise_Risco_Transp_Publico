# Funções

def formata_numero(valor):
    """
    Função customizada para formatar números com milhar e sinal de menos.
    """
    if valor >= 0:
        return '{:,.2f}'.format(valor)
    else:
        return '{:+,.2f}'.format(valor)
