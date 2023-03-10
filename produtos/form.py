from dataclasses import Field

from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Reset, Row, Submit
from django import forms

from .models import Produto


class FormProduto(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('nome'), css_class='col-md-6 col-sm-12 mb-0'),
                Column(Field('descricao'), css_class='col-md-6 col-sm-12 mb-0'),
            ),
            Row(
                Column(Field('unidade'), css_class='col-md-6 mb-0'),
                Column(Field('tipo'), css_class='col-md-6 mb-0'),
            ),
            Row(
                Column(Field(PrependedText('preco_custo', 'R$'),
                       css_class="mask_money"), css_class='form-group col-md-4 mb-0'),
                Column(Field(PrependedText('preco_delivery', 'R$'),
                       css_class="mask_money"), css_class='form-group col-md-4 mb-0'),
                Column(Field(PrependedText('preco_venda', 'R$'),
                       css_class="mask_money"), css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(Field('imagem'), css_class='col-md-12 mb-0'),
            ),
            # Row(
            #     Column(Reset('cancelar', 'Cancelar',
            #        onclick='window.location.href="{}"'.format('/produtos')),css_class='col-md-6 mb-0'),
            #     Column(Submit('submit', 'Salvar'),css_class='col-md-6 mb-0'),
            # )

        )

        self.helper.add_input(
            Reset('cancelar', 'Cancelar',
                  onclick='window.location.href="{}"'.format('/deck/produtos'))
        )
        self.helper.add_input(
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = Produto
        exclude = ['data_criacao']
