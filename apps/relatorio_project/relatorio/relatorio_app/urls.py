from django.urls import path
from . import views

urlpatterns = [
    
    #index
    path('principal/', views.home, name='home'),
    
    path('', views.index_relatorios, name='index_relatorios'),
    #Relatorios de clientes
    
    path('clientes/ativos/', views.clientes_ativos, name='clientes_ativos'),
    path('relatorios/clientes/novos/', views.novos_registros, name='novos_registros'),
    
    #Relatorios de inventarios
    path('relatorios/inventario/populares/', views.produtos_populares, name='produtos_populares'),
    path('relatorios/inventario/estoque-baixo/', views.estoque_baixo, name='estoque_baixo'),
    
    #Insights gerais
    path('relatorios/insights/gerais/', views.insights_gerais, name='insights_gerais'),
]