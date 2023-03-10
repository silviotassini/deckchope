from dataclasses import Field

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Reset, Row, Submit
from django import forms
from django.db.models import Subquery

from clientes.models import Cliente
from produtos.models import Produto, ProdutoEmprestimo


class FormEmprestimo(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.none())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.none())

    def __init__(self, user_unit, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['produto'].queryset = Produto.objects.filter(tipo=1).exclude(id__in=Subquery(ProdutoEmprestimo.objects.filter(
            datafim__isnull=True).values('produto_id')))
        if user_unit == 99:
            self.fields['cliente'].queryset = Cliente.objects.all()
        else:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                filial=user_unit)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('cliente'), css_class='col-md-6 col-sm-12 mb-0'),
            ),
            Row(
                Column(Field('produto'), css_class='col-md-6 col-sm-12 mb-0'),
            ),

        )

        self.helper.add_input(
            Reset('cancelar', 'Cancelar',
                  onclick='window.location.href="{}"'.format('/loan'))
        )
        self.helper.add_input(
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = ProdutoEmprestimo
        exclude = ['datainicio', 'datafim']
