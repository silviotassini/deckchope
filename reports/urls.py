from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.reportVendas.as_view()), name='reportVendas'),
]
