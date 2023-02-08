def formata_preco(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def cart_total_qtd(carrinho):
    if carrinho:
        return sum([item['quantidade'] for item in carrinho.values()])
    else:
        return 0


def cart_totals(carrinho):
    soma = 0
    print("="*15)
    print(carrinho)

    for item in carrinho.values():
        soma += float(item['qtd']) * float(item["preco_venda"])
    return soma


def total_pedido(itens):
    total = 0
    for item in itens:
        total += item.quantidade*item.preco
    return total
