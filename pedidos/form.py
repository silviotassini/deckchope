from dataclasses import Field
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset, Field
from crispy_forms.bootstrap import PrependedText
from .models import Pedido, ItemPedido
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime
from django.utils import timezone


class FormPedido(forms.ModelForm):

    def __init__(self, flag=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.fields['usuario'].widget = forms.HiddenInput()

        self.fields['data_entrega'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={"class": 'form-control vDateField',
                   "type": 'date',
                   "style": 'max-width: 15em'
                   }
        )
        self.fields['data_pgto'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={"class": 'form-control',
                   "type": 'date',
                   "style": 'max-width: 15em'
                   }
        )
        self.fields['obs'].widget = forms.Textarea(
            attrs={"class": 'textarea form-control',
                   "rows": '3',
                   }
        )
        self.fields['data_pedido'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={"class": 'form-control',
                   "type": 'date',
                   "style": 'max-width: 15em'
                   }
        )
        self.fields['data_pedido'].disabled = True
        self.fields['cliente'].disabled = True

        self.helper.layout = Layout(
            'usuario',
            Field('cliente', style='max-width: 35em;'),
            Row(
                Column(Field('data_pedido', style='max-width: 15em'),
                       css_class='form-group col-md-3 mb-0'),
                Column(Field('data_entrega'),
                       css_class='form-group col-md-3 mb-0'),
                css_class="justify-content-start",
            ),
            Field('data_pgto', css_class="vDateField"),
            Field('forma_pgto', style='max-width: 15em'),
            'obs',
        )

    class Meta:
        model = Pedido
        fields = ('usuario', 'cliente', 'data_pedido',
                  'data_entrega', 'data_pgto', 'forma_pgto', 'obs')
        exclude = ['data_criacao']


class FormItemPedido(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()  # imported from crispy_forms.helper
        self.form_tag = False  # solves the form tag problem

        self.helper.layout = Layout(
            'usuario',
            'produto',
            'quantidade',
            'preco'
        )

    class Meta:
        model = ItemPedido
        fields = ('produto', 'preco', 'quantidade')


class FormPedidoEntregar(forms.ModelForm):
    def clean_status(self):
        return '2'

    status = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, flag=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.fields['obs'].widget = forms.Textarea(
            attrs={"class": 'textarea form-control', "rows": '3'}
        )
        self.fields['data_entrega'].widget = forms.DateInput(
            format=("%d-%m-%Y"),
            attrs={"class": 'form-control',
                   "type": 'date',
                   "style": 'max-width: 15em'
                   }
        )
        self.helper.layout = Layout(
            Row(
                Column(Field('data_entrega'),
                       css_class='form-group col-md-6 mb-0'),
                css_class='form-row',
            ),
            'obs',
        )

    class Meta:
        model = Pedido
        fields = ('data_entrega', 'obs', 'status')


class FormPedidoPagar(forms.ModelForm):
    def clean_status(self):
        return '3'
    status = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, flag=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.fields['obs'].widget = forms.Textarea(
            attrs={"class": 'textarea form-control', "rows": '3'}
        )
        self.fields['data_pgto'].widget = forms.DateInput(
            format=('%d-%m-%Y'),
            attrs={"class": 'form-control',
                   "type": 'date',
                   "style": 'max-width: 15em'
                   }
        )
        self.helper.layout = Layout(
            Row(
                Column(Field('forma_pgto'),
                       css_class='form-group col-md-3 mb-0'),
                Column(Field('data_pgto', css_class="vDateField"),
                       css_class='form-group col-md-9 mb-0'),
                css_class='form-row',
            ),
            'obs',
        )

    class Meta:
        model = Pedido
        fields = ('data_pgto', 'forma_pgto',  'obs', 'status')


ItemPedidoFormSet = forms.inlineformset_factory(
    Pedido, ItemPedido, extra=1, can_delete=True, form=FormItemPedido)
