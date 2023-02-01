import django_tables2 as tables
from django_tables2.utils import A
import heroicons
from django.utils.html import format_html
from .models import Produto


class ProdutoHTMxTable(tables.Table):
    Excluir = tables.LinkColumn('produto_delete', text="X", args=[
                                A('pk')], attrs={'a': {'class': 'btn'}})

    def render_Excluir(self):
        return format_html(heroicons._render_icon("outline", name="trash", size=20, stroke='red'))

    class Meta:
        model = Produto
        template_name = "produtos/tables.html"
        fields = ('nome', 'descricao')
        attrs = {'class': 'table table-hover table-sm',
                 'thead': {
                     'class': 'thead-light'
                 }
                 }

        row_attrs = {
            "onClick": lambda record: "document.location.href='/deck/produtos/produto/{0}';".format(record.id)
        }
