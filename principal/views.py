import datetime
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views import View
from produtos.models import ProdutoEmprestimo
from pedidos.views import pedidosPendentes
from django.db.models import Q

from .form import FormEmprestimo


class Home(TemplateView):
    template_name = 'principal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_user_auths()
        context['entregas'] = self.process_day_of_week(
            pedidosPendentes().getEntregas())
        context['count_entregas'] = len(context['entregas'])
        context['pagtos'] = pedidosPendentes().getPagtos()
        context['count_pagtos'] = len(context['pagtos'])
        return context

    def process_day_of_week(self, q):

        for item in q:
            dia_semana = item["data_pedido"].strftime("%w")
            item["dof"] = dia_semana
        return q

    def get_user_auths(self):
        l = self.request.user.groups.values_list(
            'name', flat=True)  # QuerySet Object
        l_as_list = list(l)

        if "Unidade 01" in l_as_list:
            self.request.session['id_filial'] = 1
        elif "Unidade 02" in l_as_list:
            self.request.session['id_filial'] = 2
        elif "Unidade 03" in l_as_list:
            self.request.session['id_filial'] = 3
        elif "Admin" in l_as_list:
            self.request.session['id_filial'] = 99
        else:
            self.request.session['id_filial'] = 0
        self.request.session['filial'] = l_as_list[0]

        self.request.session.save()
        return l_as_list[0]


class Emprestimo(CreateView):
    template_name = 'principal/emprestimo.html'
    form_class = FormEmprestimo
    success_url = reverse_lazy('emprestimo')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_unit'] = self.request.session.get("id_filial")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Emprestimo, self).get_context_data(**kwargs)
        id_filial = self.request.session.get("id_filial")
        emprestimos = ProdutoEmprestimo.objects.filter(
            Q(datafim__isnull=True) & Q(cliente__filial=id_filial))
        context['emprestimos'] = emprestimos.values('id',
                                                    'cliente__nome', 'produto__nome', 'datainicio')
        return context


class Recolher(View):
    template_name = 'principal/emprestimo.html'

    def get(self, *args, **kwargs):
        id_emprestimo = kwargs['pk']
        ProdutoEmprestimo.devolver(id_emprestimo)
        return redirect(reverse_lazy('emprestimo'))

    # class createClientes(TemplateView):
    #     def dispatch(self, request, *args, **kwargs):
    #         lista = []
    #         for i in range(100):
    #             lista.append(Cliente(filial=(i % 2) + 1,
    #                                  nome="cliente " +
    #                                  str(i) + " undiade " + str((i % 2) + 1),
    #                                  razaosocial="razao social",
    #                                  tipo=(i % 2) * 1,
    #                                  cpfcnpj='',
    #                                  endereco="endereco",
    #                                  cidade='Belo Horizonte',
    #                                  uf="UF",
    #                                  email="email@gmail.com",
    #                                  phone1="31 999999991",
    #                                  phone2="31 999999992",
    #                                  obs="",
    #                                  delivery=(i % 2) * 1)
    #                          )
    #         Cliente.objects.bulk_create(lista)

    #         return super().dispatch(request, *args, **kwargs)

    # TODO: Fazer tela mostrando todos pedidos a ser entregues,
    #    permitindo fazer operacoes como entregar, pagar, etc...
    # TODO: Fazer tela mostrando todos pedidos a ser recebidos,
    #    permitindo fazer operacoes como entregar, pagar, etc...
    # TODO: Fazer tela mostrando todos pedidos vendidos por semana
