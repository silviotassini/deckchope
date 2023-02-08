from django.template import Library
from utils import utils


register = Library()


@register.filter
def formata_preco(val):
    return utils.formata_preco(val)


@register.filter
def cart_total_qtd(carrinho):
    return utils.cart_total_qtd(carrinho)


@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)


@register.filter
def keyvalue(dicionario, chave):
    return dicionario[chave]


@register.filter
def vercarrinho(carrinho):
    itens = len(carrinho)
    if itens > 1:
        return str(itens) + " itens"
    else:
        return "1 item"
