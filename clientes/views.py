# Create your views here.
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import View
from django.urls import reverse_lazy
from django.http import HttpResponse
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
    paginate_by = 5

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

    # substitui por um manager no models
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     id_filial = self.request.session.get('id_filial')
    #     if id_filial in [1,2]:
    #         queryset = queryset.filter(filial=id_filial)
    #     return queryset


class ClienteDetalhe(SuccessMessageMixin, UpdateView):
    model = Cliente
    form_class = FormCliente
    context_object_name = 'cliente'
    success_url = "/clientes"
    success_message = "Cliente [%(nome)s] atualizado com sucesso!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: voltar o request quando colocar login
        self.object.filial = self.request.session.get("id_filial")
        self.object.save()
        return super(ClienteCreate, self).form_valid(form)


class ClienteCreate(SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = FormCliente
    form_class.base_fields['tipo'].initial = 1
    success_url = reverse_lazy('clientes')
    success_message = "Cliente [%(nome)s] foi criado com sucesso!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: voltar o request quando colocar login
        self.object.filial = self.request.session.get("id_filial")
        self.object.save()
        return super(ClienteCreate, self).form_valid(form)


class ClienteDelete(SuccessMessageMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('clientes')
    success_message = "Registro de cliente apagado!"


class ClienteLista(SingleTableMixin, FilterView):
    table_class = ClienteHTMxTable
    # queryset = Cliente.objects.all()
    filterset_class = ClienteFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "clientes/cliente_table_lista_partial.html"
        else:
            template_name = "clientes/cliente_table_lista.html"
        return template_name


# TODO: em vez de criar dois html para cliente tble, ver como passar parametro no cliente filter

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("clienteid"):
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('venda'))

    def get_table_kwargs(self):
        return {'exclude': ('Excluir', 'Tabela'), "row_attrs": {"onClick": lambda record: "document.location.href='/deck/clientes/lista/{0}';".format(record.id)}}


class ClienteSelect(View):

    def get(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(id=kwargs.get('pk'))
        request.session['clienteid'] = cliente.id
        request.session['cliente'] = cliente.nome
        request.session['delivery'] = cliente.delivery
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
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
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
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.cliente_id = self.kwargs['pk']
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
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        clienteid = self.kwargs['pk']
        return reverse_lazy('cliente_precos', kwargs={'pk': clienteid})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
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
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        clienteid = self.kwargs['pk']
        return reverse_lazy('cliente_precos', kwargs={'pk': clienteid})
