from dataclasses import Field
from django import forms
from .models import Pedido, ItemPedido
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime

class FormPedido(forms.ModelForm):                    
                 
    class Meta:
        model = Pedido
        exclude = ['data_criacao']

class FormItemPedido(forms.ModelForm):

    class Meta:            
        model = ItemPedido
        fields = ('produto', 'preco', 'quantidade')

ItemPedidoFormSet = forms.inlineformset_factory(Pedido, ItemPedido, extra=1, can_delete=False, form=FormItemPedido)            