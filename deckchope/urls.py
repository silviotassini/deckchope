from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')),
    path('produtos/', include('produtos.urls')),
    path('clientes/', include('clientes.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
