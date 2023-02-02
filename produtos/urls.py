from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views


urlpatterns = [
    path('', login_required(views.ProdutoHTMxTableView.as_view()), name='produtos'),
    path('produto/<int:pk>', login_required(views.ProdutoDetalhe.as_view()),
         name='produto_detail'),
    path('produto/', login_required(views.ProdutoCreate.as_view()),
         name='produto_create'),
    path('produto/<int:pk>/delete',
         login_required(views.ProdutoDelete.as_view()), name='produto_delete'),
    path('show/', login_required(views.ProdutoShow.as_view()), name='produto_show'),
    path('carrinho/', login_required(views.ProdutoCarrinho.as_view()), name='carrinho'),
    path('carrinho/<int:pk>/delete',
         login_required(views.DeleteProdutoCarrinho.as_view()), name='remove_item_carrinho'),
    path('show/stopvenda',
         login_required(views.ProdutoStopVenda.as_view()), name='stop_venda'),
]
