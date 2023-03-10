from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.Home.as_view()), name='home'),
    path('loan/',
         login_required(views.Emprestimo.as_view()), name='emprestimo'),
    path('refund/<int:pk>',
         login_required(views.Recolher.as_view()), name='recolher'),
    # path('criaclientes', login_required(
    #     views.createClientes.as_view()), name='criaclientes'),
]
