from django.contrib.auth.decorators import login_required
from django.urls import include, path

from . import views

urlpatterns = [
    path('', login_required(views.ClienteHTMxTableView.as_view()), name='clientes'),
    path('cliente/<int:pk>', login_required(views.ClienteDetalhe.as_view()),
         name='cliente_detail'),
    path('cliente/', login_required(views.ClienteCreate.as_view()),
         name='cliente_create'),
    path('cliente/<int:pk>/delete',
         login_required(views.ClienteDelete.as_view()), name='cliente_delete'),
    path('lista/', login_required(views.ClienteLista.as_view()), name='venda'),
    path('lista/<int:pk>/', login_required(views.ClienteSelect.as_view())),
    path('<int:pk>/tabela/', login_required(views.ClientePrecos.as_view()),
         name='cliente_precos'),
    path('<int:pk>/tabela/<int:sk>', login_required(views.ClienteUpdatePrecos.as_view()),
         name='cliente_update_precos'),
    path('<int:pk>/tabela/<int:sk>/delete',
         login_required(views.ClientePrecosDelete.as_view()), name='cliente_update_precos'),
]
