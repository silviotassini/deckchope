from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.Home.as_view()), name='home'),
    # path('criaclientes', login_required(
    #     views.createClientes.as_view()), name='criaclientes'),
]
