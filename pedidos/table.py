import django_tables2 as tables
from django_tables2.utils import A
import heroicons 
from django.utils.html import format_html
from .models import Pedido

class PedidoHTMxTable(tables.Table):
    Entregar = tables.LinkColumn('pedido_entregar', text="D", args=[A('pk')], 
                                    attrs={'a': {'class': 'btn'} },
                                    verbose_name="Confirmar entrega")

    Pagar = tables.LinkColumn('pedido_pagar', text="$", args=[A('pk')], 
                                    attrs={'a': {'class': 'btn'} })

    Excluir = tables.LinkColumn('pedido_delete', text="X", args=[A('pk')], 
                                    attrs={'a': {'class': 'btn'} })
    
    def render_Entregar(self):
        return format_html( heroicons._render_icon("outline", name="truck",size=20,stroke='blue'))

    def render_Excluir(self):
        return format_html( heroicons._render_icon("outline", name="trash",size=20,stroke='red'))

    def render_Pagar(self):
        return format_html( heroicons._render_icon("outline", name="currency-dollar",size=20,stroke='green'))

    class Meta:
        model = Pedido
        template_name = "pedidos/tables.html"
        fields = ('cliente', 'data_pedido','data_entrega')
        attrs = {   'class': 'table table-hover table-sm',
                    'thead' : {
                        'class': 'thead-light'
                    }
                }

        row_attrs = {
            "onClick": lambda record: "document.location.href='/pedidos/pedido/{0}';".format(record.id)
        }
        