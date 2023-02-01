from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProdutoHTMxTableView.as_view(), name='produtos'),
    path('produto/<int:pk>', views.ProdutoDetalhe.as_view(), name='produto_detail'),
    path('produto/', views.ProdutoCreate.as_view(), name='produto_create'),
    path('produto/<int:pk>/delete',
         views.ProdutoDelete.as_view(), name='produto_delete'),
    path('show/', views.ProdutoShow.as_view(), name='produto_show'),
    path('carrinho/', views.ProdutoCarrinho.as_view(), name='carrinho'),
    path('carrinho/<int:pk>/delete',
         views.DeleteProdutoCarrinho.as_view(), name='remove_item_carrinho'),
    path('show/stopvenda', views.ProdutoStopVenda.as_view(), name='stop_venda'),
]
