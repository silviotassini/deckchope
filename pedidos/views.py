# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from produtos.models import Produto
from .models import Pedido, ItemPedido
from clientes.models import Cliente, ClienteTabela
from .form import FormPedido, FormItemPedido, FormPedidoEntregar, FormPedidoPagar
from pedidos.table import PedidoHTMxTable
from pedidos.filter import PedidoFilter
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from utils import utils


class PedidoHTMxTableView(SingleTableMixin, FilterView):
    table_class = PedidoHTMxTable
    queryset = Pedido.objects.all()
    filterset_class = PedidoFilter
    paginate_by = 5

    def get_template_names(self):
        if self.request.htmx:
            template_name = "pedidos/pedido_table_partial.html"
        else:
            template_name = "pedidos/pedido_table.html"
        return template_name


class pedidosPendentes(TemplateView):

    def getEntregas(self):
        entregar = Pedido.objects.select_related().filter(status=1).values(
            'pk', 'cliente', 'data_pedido', 'cliente__nome')
        return entregar

    def getPagtos(self):
        pagar = Pedido.objects.select_related().filter(data_pgto__isnull=True).values(
            'pk', 'cliente', 'data_pedido', 'cliente__nome')
        return pagar


class PedidoEntregarView(SingleTableMixin, FilterView):
    table_class = PedidoHTMxTable
    queryset = Pedido.objects.filter(status=1)
    filterset_class = PedidoFilter
    paginate_by = 5

    def get_template_names(self):
        if self.request.htmx:
            template_name = "pedidos/pedido_table_partial.html"
        else:
            template_name = "pedidos/pedido_table.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pedido"] = self.queryset
        return context


class PedidoPagarView(PedidoHTMxTableView, pedidosPendentes):
    pass


class ItemPedidoInline(InlineFormSetFactory):
    model = ItemPedido
    fields = ['produto', 'preco', 'quantidade']
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}


class PedidoCreate(SuccessMessageMixin, CreateWithInlinesView):
    model = Pedido
    inlines = [ItemPedidoInline,]
    form_class = FormPedido
    success_url = '/pedidos'
    success_message = "Pedido criado com sucesso!"

    def get_initial(self):
        return {
            "usuario": "1"  # self.request.user,
        }


class BaseCarrinho(View):
    def RemoveProdutoCarrinho(self, carrinho):
        tmp = {k: v for k, v in carrinho.items() if int(carrinho[k]) != 0}
        self.request.session['carrinho'] = tmp
        self.request.session.save()

    def get_object(self):
        obj = ClienteTabela.objects.filter(
            cliente_id=self.request.session.get("clienteid")).select_related("produto")
        return obj

    def ProcessaCarrinho(self, carrinho):
        tmp = {int(k): v for k, v in carrinho.items()}
        carrinhoItens = {}
        carrinhoItens2 = {}
        for k, v in tmp.items():
            produto = self.get_object().filter(produto_id=k)
            print(produto[0].produto.nome)
            carrinhoItens[k] = {
                "id": k,
                "nome": produto[0].produto.nome,
                "preco_venda": produto[0].preco,
                "tipo": produto[0].produto.tipo,
                "qtd": v
            }
            carrinhoItens2[k] = {
                "qtd": str(v),
                "preco": str(produto[0].preco)
            }
        return [carrinhoItens, carrinhoItens2]


class PedidoVendas(TemplateView, BaseCarrinho):
    template_name = "pedidos/vendas.html"

    def get(self, *args, **kwargs):
        context = {}
        if self.request.session.get('carrinho'):
            [carrinhoItens, carrinhoItens2] = self.ProcessaCarrinho(
                self.request.session.get('carrinho')
            )
            context = {"carrinhoItens": carrinhoItens}
            self.request.session['carrinhoItens'] = carrinhoItens2
            self.request.session.save()

        return render(self.request, self.template_name, context=context)


class DeleteProdutoCarrinho(BaseCarrinho):

    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')
        pk = str(kwargs['pk'])
        self.request.session['carrinho'][pk] = 0
        self.request.session.save()
        self.RemoveProdutoCarrinho(carrinho)
        return redirect(self.request.META.get('HTTP_REFERER'))


class PedidoDetalhe(SuccessMessageMixin, UpdateWithInlinesView):
    model = Pedido
    inlines = [ItemPedidoInline,]
    form_class = FormPedido
    context_object_name = 'Pedido'
    success_url = reverse_lazy('pedidos')
    success_message = "Pedido atualizado com sucesso!"


class PedidoDelete(SuccessMessageMixin, DeleteView):
    model = Pedido
    success_url = reverse_lazy('pedidos')
    success_message = "Registro de Pedido apagado!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = ItemPedido.objects.filter(pedido_id=self.kwargs['pk'])
        context["itens"] = itens
        return context


class PedidoEntregar(SuccessMessageMixin, UpdateView):
    model = Pedido
    form_class = FormPedidoEntregar
    context_object_name = 'pedido'
    success_url = reverse_lazy('pedidos')
    success_message = "Pedido registrado como entregue!"
    template_name = 'pedidos/pedido_confirm_entregar.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        itens = ItemPedido.objects.filter(pedido_id=self.kwargs['pk'])
        context["itens"] = itens
        return render(request, self.template_name, context)


class PedidoPagar(SuccessMessageMixin, UpdateView):
    model = Pedido
    form_class = FormPedidoPagar
    context_object_name = 'pedido'
    success_url = reverse_lazy('pedidos')
    success_message = "Pagamento de Pedido registrado com sucesso!"
    template_name = 'pedidos/pedido_confirm_pagar.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        itens = ItemPedido.objects.filter(pedido_id=self.kwargs['pk'])
        context["total_pedido"] = utils.total_pedido(itens)
        return render(request, self.template_name, context)


class PedidoNovo(SuccessMessageMixin, CreateView):
    form_class = FormPedido
    success_url = reverse_lazy('pedidos')
    success_message = "Pedido foi criado com sucesso!"
    model = Pedido

    def form_valid(self, form):
        self.object = form.save()
        # itempedido = ItemPedido()
        carrinhoItens = self.request.session.get('carrinhoItens')

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido_id=self.object.id,
                    produto_id=int(k),
                    preco=float(v['preco']),
                    quantidade=int(v['qtd'])
                ) for k, v in carrinhoItens.items()
            ]
        )
        del self.request.session['carrinhoItens']
        del self.request.session['carrinho']
        del self.request.session['clienteid']
        del self.request.session['cliente']
        del self.request.session['delivery']
        return HttpResponseRedirect(self.get_success_url())

    def get_template_names(self):
        template_name = "pedidos/pedido_novo.html"
        return template_name

    def get_initial(self):
        self.cliente = Cliente.objects.get(
            id=self.request.session.get("clienteid"))
        return {
            "usuario": self.request.user,
            "cliente": self.cliente
        }


class PedidoPararVenda(View):
    def get(self, *args, **kwargs):
        del self.request.session['clienteid']
        del self.request.session['cliente']
        if self.request.session.get('carrinho'):
            del self.request.session['carrinho']
        self.request.session.save()
        return redirect(reverse_lazy('venda'))


class ProdutoShow(ListView, BaseCarrinho):
    model = Produto
    template_name = "produtos/produto_show.html"
    context_object_name = 'produtos'
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        obj = ClienteTabela.objects.filter(
            cliente_id=self.request.session.get("clienteid")).select_related("produto")
        return obj

    def get_context_data(self, **kwargs):
        context = super(ProdutoShow, self).get_context_data(**kwargs)
        if self.request.session.get('carrinho'):
            tmp = self.request.session.get('carrinho')
            carrinho = {int(k): v for k, v in tmp.items()}
            context['carrinho'] = carrinho
        return context

    def post(self, request, *args, **kwargs):

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        pid = self.request.POST.get("pid")

        carrinho = self.request.session['carrinho']
        carrinho[pid] = self.request.POST.get("qtd")

        self.RemoveProdutoCarrinho(carrinho)

        success_message = "Produto adicionado!"
        # messages.success(self.request, success_message)

        return redirect(self.request.META.get('HTTP_REFERER'))
