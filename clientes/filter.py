
from django.db.models import Q
import django_filters
from .models import Cliente
from django.forms.widgets import TextInput


class ClienteFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="",
                                      widget=TextInput(attrs={'placeholder': 'pesquisar por...', 'class': 'shadow p-2 bg-white rounded'}))

    class Meta:
        model = Cliente
        fields = ['query']

    @property
    def qs(self):
        parent = super().qs
        filial = self.request.session.get("id_filial")
        if filial in [1, 2]:
            queryset = parent.filter(filial=filial)
        else:
            queryset = parent
        return queryset

    def universal_search(self, queryset, name, value):
        """         
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return Cliente.objects.filter(
                Q(price=value) | Q(cost=value)
            ) """

        if self.request.session.get('id_filial') in ['1', '2']:
            return Cliente.objects.filter(
                Q(filial=self.request.session['id_filial']) | Q(
                    nome__icontains=value)
            )
        else:
            return Cliente.objects.filter(
                Q(nome__icontains=value)
            )
