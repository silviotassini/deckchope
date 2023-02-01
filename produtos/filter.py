# products/filters.py
from django.db.models import Q
import django_filters
from .models import Produto
from django.forms.widgets import TextInput

class ProdutoFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="", 
                    widget=TextInput(attrs={'placeholder': 'pesquisar por...','class': 'shadow p-2 bg-white rounded'}))

    class Meta:
        model = Produto
        fields = ['query']

    # @property
    # def qs(self):
    #     parent = super().qs
    #     filial = self.request.session.get("id_filial")
    #     if filial in [1,2]:
    #         queryset = parent.filter(filial=filial)
    #     else:
    #         queryset = parent
    #     return queryset

    def universal_search(self, queryset, name, value):

        return Produto.objects.filter(
            Q(nome__icontains=value) | Q(descricao__icontains=value)
        )
