# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Produto
from .form import FormProduto
from produtos.table import ProdutoHTMxTable
from produtos.filter import ProdutoFilter
from PIL import Image


class ProdutoHTMxTableView(SingleTableMixin, FilterView):
    table_class = ProdutoHTMxTable
    queryset = Produto.objects.all()
    filterset_class = ProdutoFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "produtos/produto_table_partial.html"
        else:
            template_name = "produtos/produto_table.html"
        # template_name = "produtos/produto_table_partial.html"
        return template_name


class ProdutoDetalhe(SuccessMessageMixin, UpdateView):
    model = Produto
    form_class = FormProduto
    context_object_name = 'produto'
    success_url = reverse_lazy('produtos')
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
