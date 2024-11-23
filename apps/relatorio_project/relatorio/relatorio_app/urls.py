from django.urls import path
from . import views

urlpatterns = [
    
    #index
    path('', views.home, name='home'),
    
    path('relatorios/', views.index_relatorios, name='index_relatorios'),
    #Relatorios de clientes
    
    path('clientes/ativos/', views.clientes_ativos, name='clientes_ativos'),
    path('clientes/novos/', views.novos_registros, name='novos_registros'),
    
    #Relatorios de inventarios
    path('inventario/populares/', views.produtos_populares, name='produtos_populares'),
    path('inventario/estoque-baixo/', views.estoque_baixo, name='estoque_baixo'),
    
    #Insights gerais
    path('insights/gerais/', views.insights_gerais, name='insights_gerais'),
]