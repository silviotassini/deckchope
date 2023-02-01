# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Produto
#from clientes.models import Cliente, ClienteTabela
from .form import FormProduto
from produtos.table import ProdutoHTMxTable
from produtos.filter import ProdutoFilter
from PIL import Image


class ProdutoHTMxTableView(SingleTableMixin, FilterView):
    table_class = ProdutoHTMxTable
    queryset = Produto.objects.all()
    filterset_class = ProdutoFilter
    paginate_by = 5

    def get_template_names(self):
        if self.request.htmx:
            template_name = "produtos/produto_table_partial.html"
        else:
            template_name = "produtos/produto_table.html"
        #template_name = "produtos/produto_table_partial.html"
        return template_name


class ProdutoDetalhe(SuccessMessageMixin, UpdateView):
    model = Produto
    form_class = FormProduto
    context_object_name = 'produto'
    success_url = "/produtos"
    success_message = "Produto [%(nome)s] atualizado com sucesso!"


class ProdutoCreate(SuccessMessageMixin, CreateView):
    model = Produto
    form_class = FormProduto
    success_url = reverse_lazy('produtos')
    success_message = "Produto [%(nome)s] foi criado com sucesso!"


class ProdutoDelete(SuccessMessageMixin, DeleteView):
    model = Produto  
    success_url = reverse_lazy('produtos')
    success_message = "Registro de produto apagado!"


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

class ProdutoStopVenda(View):
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
        #messages.success(self.request, success_message)
        #del self.request.session['carrinho']
        return redirect(self.request.META.get('HTTP_REFERER'))


class DeleteProdutoCarrinho(BaseCarrinho):

    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')
        pk = str(kwargs['pk'])
        self.request.session['carrinho'][pk] = 0
        self.request.session.save()
        self.RemoveProdutoCarrinho(carrinho)
        return redirect(self.request.META.get('HTTP_REFERER'))


class ProdutoCarrinho(BaseCarrinho):
    template_name = "produtos/carrinho.html"

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
