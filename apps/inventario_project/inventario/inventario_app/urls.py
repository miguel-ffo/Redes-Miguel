from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('adicionar/', views.cria_produto, name='cria_produto'),
    path('editar/<int:id>/', views.edita_produto, name='edita_produto'),
    path('deletar/<int:id>/', views.deleta_produto, name='deleta_produto'),
    path('executar-query/', views.executar_query, name='executar_query'),
]