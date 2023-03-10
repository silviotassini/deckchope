# Create your views here.
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import View
from django.urls import reverse_lazy
from .models import Cliente, ClienteTabela
from .form import FormCliente, FormClienteTabela, TabelaCliente
from clientes.table import ClienteHTMxTable
from clientes.filter import ClienteFilter
# from extra_views import (
#     CreateWithInlinesView,
#     UpdateWithInlinesView,
#     InlineFormSetFactory,
# )


class ClienteHTMxTableView(SingleTableMixin, FilterView):
    table_class = ClienteHTMxTable
    filterset_class = ClienteFilter
    paginate_by = 15

    def get_table_kwargs(self, Excluir=True):
        if Excluir == True:
            return {"row_attrs": {"onClick": lambda record: "document.location.href='/deck/clientes/cliente/{0}';".format(record.id)}}
        else:
            return {'exclude': ('Excluir',)}

    def get_template_names(self):
        if self.request.htmx:
            template_name = "clientes/cliente_table_partial.html"
        else:
            template_name = "clientes/cliente_table.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super(ClienteHTMxTableView, self).get_context_data(**kwargs)
        context["txtHeader"] = "Clientes"
        return context


class ClienteDetalhe(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = FormCliente
    context_object_name = 'cliente'
    success_url = reverse_lazy('clientes')
    success_message = "Cliente [%(nome)s] atualizado com sucesso!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_unit'] = self.request.session.get("id_filial")
        return kwargs


class ClienteCreate(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = FormCliente
    form_class.base_fields['tipo'].initial = 1
    success_url = reverse_lazy('clientes')
    success_message = "Cliente [%(nome)s] foi criado com sucesso!"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_unit'] = self.request.session.get("id_filial")
        return kwargs

    def get_initial(self):
        return {
            "filial": self.request.session.get("id_filial"),
        }


class ClienteDelete(SuccessMessageMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('clientes')
    success_message = "Registro de cliente apagado!"


class ClienteLista(SingleTableMixin, FilterView):
    table_class = ClienteHTMxTable
    filterset_class = ClienteFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "clientes/cliente_table_lista_partial.html"
        else:
            template_name = "clientes/cliente_table_lista.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super(ClienteLista, self).get_context_data(**kwargs)
        context["txtHeader"] = "Selecione Cliente para o pedido"
        return context
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get("clienteid"):
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect(reverse_lazy('venda'))

    def get_table_kwargs(self):
        return {'exclude': ('Excluir', 'Tabela'), "row_attrs": {"onClick": lambda record: "document.location.href='/deck/clientes/lista/{0}';".format(record.id)}}


class ClienteSelect(View):

    def get(self, request, *args, **kwargs):
        #cliente = Cliente.objects.get(id=kwargs.get('pk'))
        cliente = Cliente.objects.select_related().get(id=kwargs.get('pk'))
        request.session['clienteid'] = cliente.id
        request.session['cliente'] = cliente.nome
        request.session['delivery'] = cliente.delivery
        produtosCliente = cliente.clientetabela_set.all()
        request.session.save()
        return redirect(reverse_lazy('venda'))


class ClienteBasePrecos(View):
    model = ClienteTabela
    cliente = None

    def get_itens(self, cliente_id):
        self.cliente = Cliente.objects.get(id=cliente_id)
        lista = self.cliente.clientetabela_set.all()
        itens = []
        for item in lista:
            d = {}
            d["id"] = item.datacsv().split(";")[0]
            d["produto"] = item.datacsv().split(";")[2]
            d["preco"] = float(item.datacsv().split(";")[3])
            itens.append(d)
        return [itens, self.cliente]


class ClientePrecos(SuccessMessageMixin, CreateView, ClienteBasePrecos):
    model = ClienteTabela
    form_class = FormClienteTabela
    template_name = "clientes/cliente_tabela.html"
    success_message = "Item salvo com sucesso!"
    cliente = None

    def get_success_url(self):
        clienteid = self.kwargs['pk']
        return reverse_lazy('cliente_precos', kwargs={'pk': clienteid})

    def get_context_data(self, **kwargs):
        context = super(ClientePrecos, self).get_context_data(**kwargs)
        itens = self.get_itens(self.kwargs['pk'])[0]
        context['cliente'] = self.get_itens(self.kwargs['pk'])[1]
        context['cliente_id'] = self.kwargs['pk']
        context["PrecoCliente"] = itens
        return context

    def form_valid(self, form):
        form.instance.cliente_id = self.kwargs['pk']
        from django.db import connection
        return super().form_valid(form)


class ClienteUpdatePrecos(SuccessMessageMixin, UpdateView, ClienteBasePrecos):
    model = ClienteTabela
    form_class = FormClienteTabela
    template_name = "clientes/cliente_tabela.html"
    success_message = "Item salvo com sucesso!"
    cliente = None

    def get_object(self):
        obj = self.model.objects.get(id=self.kwargs['sk'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdatePrecos, self).get_context_data(**kwargs)
        itens = self.get_itens(self.kwargs['pk'])[0]
        context['cliente'] = self.get_itens(self.kwargs['pk'])[1]
        context['cliente_id'] = self.kwargs['pk']
        context["PrecoCliente"] = itens
        return context

    def get_success_url(self):
        clienteid = self.kwargs['pk']
        return reverse_lazy('cliente_precos', kwargs={'pk': clienteid})

    def form_valid(self, form):
        form.instance.cliente_id = self.kwargs['pk']
        return super().form_valid(form)


class ClientePrecosDelete(SuccessMessageMixin, DeleteView):
    model = ClienteTabela
    success_message = "Registro apagado!"
    template_name = "clientes/clienteprecos_confirm_delete.html"

    def get_object(self):
        obj = self.model.objects.get(id=self.kwargs['sk'])
        return obj

    def get_success_url(self):
        clienteid = self.kwargs['pk']
        return reverse_lazy('cliente_precos', kwargs={'pk': clienteid})
