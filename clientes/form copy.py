from dataclasses import Field

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Reset, Row, Submit
from django import forms

from produtos.models import Produto

from .models import Cliente, ClienteTabela


class FormCliente(forms.ModelForm):

    def __init__(self, user_unit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.HTTP_REFERER = kwargs.pop('http_referer')
        if user_unit in [1, 2]:
            self.fields['filial'].widget = forms.HiddenInput()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('filial', style='max-width: 30em'),
            'delivery',
            Row(Column(Field('nome', style='max-width: 30em'), css_class='form-group col-md-3 mb-0'),
                # Column(Field('razaosocial', style='max-width: 30em'),css_class='form-group col-md-3 mb-0'),
                css_class="justify-content-start"
                ),
            Row(Column(Field('tipo', style='max-width: 15em'), css_class='form-group col-md-3 mb-0'),
                Column(Field('cpfcnpj', style='max-width: 20em', css_class='mask_cpfcnpj'),
                       css_class='form-group col-md-3 mb-0'),
                # Column(Field('rgie', style='max-width: 15em'), css_class='form-group col-md-3 mb-0'),
                css_class="justify-content-start"
                ),
            Row(Column(Field('endereco', style='max-width: 30em'), css_class='form-group col-md-3 mb-0'),
                Column(Field('bairro', style='max-width: 30em'),
                       css_class='form-group col-md-3 mb-0'), css_class="justify-content-start"
                ),
            Row(Column(Field('complemento', style='max-width: 30em'),
                       css_class='form-group col-md-3 mb-0'),
                Column(Field('numero', style='max-width: 8em'),
                       css_class='form-group col-md-3 mb-0'),
                Column(Field('cep', style='max-width: 8em', css_class='mask_cep'),
                       css_class='form-group col-md-3 mb-0'), css_class="justify-content-start"
                ),
            Row(
                # Column(Field('uf', style='max-width: 15em'), css_class='form-group col-md-3 mb-0'),
                Column(Field('cidade', style='max-width: 30em'),
                       css_class='form-group col-md-3 mb-0'), css_class="justify-content-start"
            ),

            Field('email', style='max-width: 30em'),
            Row(Column(Field('phone1', style='max-width: 15em',
                             css_class='mask_telefone'), css_class='form-group col-md-3 mb-0'),
                Column(Field('phone2', style="max-width: 15em",
                             css_class='mask_telefone'),
                       css_class='form-group col-md-3 mb-0'), css_class="justify-content-start"
                ),
        )
        self.helper.add_input(
            # ,onclick='window.location.href="'+ self.HTTP_REFERER + '"')
            Reset('cancelar', 'Cancelar',
                  onclick='window.location.href="{}"'.format('/deck/clientes'))
        )
        self.helper.add_input(
            Submit('submit', 'Salvar')
        )

    def clean(self):
        data = self.cleaned_data

    #     nome = data.get("nome")
    #     comentario = data.get("comentario")
    #     email = data.get("email")
    #     if len(nome) < 3:
    #         self.add_error(
    #             'nome',
    #             'Tamanho do campo nome inconsistente'
    #         )

    class Meta:
        model = Cliente
        # fields = ('nome','email','comentario')
        exclude = ['data_criacao']


class FormClienteTabela(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(tipo=0)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('produto', style='max-width: 30em'),
            Field('preco', style='max-width: 30em'),
        )
        self.helper.add_input(
            Reset('cancelar', 'Cancelar',
                  onclick='window.location.href="{}"'.format(
                      '/deck/clientes', css_class="btn btn-inverse")
                  )
        )
        self.helper.add_input(
            Submit('submit', 'Salvar', css_class="btn btn-primary")
        )

    class Meta:
        model = ClienteTabela
        fields = ("produto", "preco",)
        widgets = {
            'preco': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


TabelaCliente = forms.models.inlineformset_factory(Cliente, ClienteTabela,
                                                   form=FormClienteTabela, fields=(
                                                       'produto', 'preco',),
                                                   extra=1, can_delete=True)
