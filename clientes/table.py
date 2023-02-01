import django_tables2 as tables
import heroicons
from django.utils.html import format_html
from django_tables2.utils import A

from .models import Cliente


class ClienteHTMxTable(tables.Table):
    Tabela = tables.LinkColumn('cliente_precos', text="$", args=[
                               A('pk')], attrs={'a': {'class': 'btn'}})
    Excluir = tables.LinkColumn('cliente_delete', text="x", args=[
                                A('pk')], attrs={'a': {'class': 'btn'}})
    nomeCliente = tables.Column(accessor='nomeCliente', verbose_name='Cliente')

    def render_Tabela(self):
        return format_html(heroicons._render_icon("outline", name="currency-dollar", size=20, stroke='blue'))

    def render_Excluir(self):
        return format_html(heroicons._render_icon("outline", name="trash", size=20, stroke='red'))

    class Meta:
        model = Cliente
        template_name = "clientes/tables.html"
        fields = ('nomeCliente', 'phone1')
        attrs = {'class': 'table table-hover table-sm',
                 'thead': {
                     'class': 'thead-light'
                 },
                 }
        # row_attrs = {
        #     "onClick": lambda record: "document.location.href='/deck/clientes/cliente/{0}';".format(record.id)
        # }
