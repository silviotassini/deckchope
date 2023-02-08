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
]
