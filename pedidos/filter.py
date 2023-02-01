# products/filters.py
from django.db.models import Q
import django_filters
from .models import Pedido
from django.forms.widgets import TextInput

class PedidoFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="", 
                    widget=TextInput(attrs={'placeholder': 'pesquisar por...','class': 'shadow p-2 bg-white rounded'}))

    class Meta:
        model = Pedido
        fields = ['query']

    @property
    def qs(self):
        parent = super().qs
        filial = self.request.session.get("id_filial")
        if filial in [1,2]:
            queryset = parent.filter(cliente__filial=filial)
        else:
            queryset = parent
        return queryset

    def universal_search(self, queryset, name, value):
        return Produto.objects.filter(            
            Q(cliente__icontains=value) | Q(obs__icontains=value)        )
