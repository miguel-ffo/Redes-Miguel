from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes,name='lista_clientes'),
    path('adicionar/', views.cria_cliente, name='cria_cliente'),
    path('editar/<int:id>/', views.edita_cliente, name='edita_cliente'),
    path('deletar/<int:id>/', views.deleta_cliente, name='deleta_cliente'),
]