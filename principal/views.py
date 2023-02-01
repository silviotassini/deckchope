from django.shortcuts import render
from django.views.generic.base import TemplateView
#from pedidos.views import pedidosPendentes
from django.conf import settings


class Home(TemplateView):
    template_name = 'principal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['entregas'] = pedidosPendentes().getEntregas()
        # context['count_entregas'] = len(context['entregas'])
        # context['pagtos'] = pedidosPendentes().getPagtos()
        # context['count_pagtos'] = len(context['pagtos'])
        # context['filial'] = self.get_user_auths()
        context['basedir'] = settings.BASE_DIR
        return context

    def get_user_auths(self):
        l = self.request.user.groups.values_list(
            'name', flat=True)  # QuerySet Object
        l_as_list = list(l)
        if "Unidade 01" in l_as_list:
            self.request.session['id_filial'] = 1
        elif "Unidade 02" in l_as_list:
            self.request.session['id_filial'] = 2
        elif "Admin" in l_as_list:
            self.request.session['id_filial'] = 99
        else:
            self.request.session['id_filial'] = 0
        self.request.session['filial'] = l_as_list[0]
        self.request.session.save()
        return l_as_list[0]


# TODO: Fazer tela mostrando todos pedidos a ser entregues,
#    permitindo fazer operacoes como entregar, pagar, etc...
# TODO: Fazer tela mostrando todos pedidos a ser recebidos,
#    permitindo fazer operacoes como entregar, pagar, etc...
# TODO: Fazer tela mostrando todos pedidos vendidos por semana
