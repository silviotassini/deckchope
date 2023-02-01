from django.contrib import admin
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline,
    ]

# Register your models here.
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)