from django.contrib import admin
from .models import Produto, ProdutoEstoque

# Register your models here.
# class ClienteAdmin(admin.ModelAdmin):
#    list_display = ('id','nome','razaosocial','phone1')
#    list_display_links = ('id','nome')

admin.site.register(Produto)  # , ClienteAdmin)
admin.site.register(ProdutoEstoque)
