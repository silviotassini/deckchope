def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    if carrinho:
        return sum([item['quantidade'] for item in carrinho.values()])
    else:
        return 0

def cart_totals(carrinho, tipo):
    soma = 0    
    for item in carrinho.values():
        if tipo:
            soma += float(item['qtd']) * float(item["preco_delivery"])
        else:
            soma += float(item['qtd']) * float(item["preco_venda"])
    return soma

def total_pedido(itens):
    total=0
    for item in itens:
        total += item.quantidade*item.preco
    return total