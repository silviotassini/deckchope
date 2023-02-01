from django.contrib import admin
from .models import Cliente, ClienteTabela

class ItemClienteTabela(admin.TabularInline):
    model = ClienteTabela

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nome','razaosocial','phone1')
    list_display_links = ('id','nome')
    inlines = [
        ItemClienteTabela,
    ]
    
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteTabela)

