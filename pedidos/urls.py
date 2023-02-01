from django.contrib.auth.decorators import login_required
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.PedidoHTMxTableView.as_view(), name='pedidos'),    
    path('pedido/<int:pk>', views.PedidoDetalhe.as_view(), name='pedido_detail'),
    path('pedido/', views.PedidoCreate.as_view(), name='pedido_create'),
    path('pedido/<int:pk>/delete', views.PedidoDelete.as_view(), name='pedido_delete'), 
    path('pedido/<int:pk>/entregar', views.PedidoEntregar.as_view(), name='pedido_entregar'), 
    path('pedido/<int:pk>/pagar', views.PedidoPagar.as_view(), name='pedido_pagar'),     
    path('pedido/novo/', views.PedidoNovo.as_view(), name='pedido_novo'),
    path('pedido/pendencias/1/', views.PedidoEntregarView.as_view(), name='pedido_entregas_pendentes'),
    path('pedido/pendencias/2/', views.PedidoPagarView.as_view(), name='pedido_pagtos_pendentes'),
]