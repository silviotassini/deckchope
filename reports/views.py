from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views import View
from produtos.models import ProdutoEmprestimo
from django.db.models import Q


# TODO: relatorio venda que possa filtrar por periodo/por cliente
# TODO: relatorio de pagto recebidos por periodo
# TODO: relatorio mostrando chopeiras emprestadas
# TODO: relatorio mostrando historico da chopeira
# TODO: produtos mais vendidos por periodo
# TODO: clientes que mais compraram num periodo
# TODO:

class reportVendas(TemplateView):
    template_name = 'reports/vendas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_user_auths()
        context['entregas'] = self.process_day_of_week(
            pedidosPendentes().getEntregas())
        context['count_entregas'] = len(context['entregas'])
        context['pagtos'] = pedidosPendentes().getPagtos()
        context['count_pagtos'] = len(context['pagtos'])
        return context
