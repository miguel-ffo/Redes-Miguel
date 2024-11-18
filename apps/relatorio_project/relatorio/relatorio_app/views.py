from django.shortcuts import render
from datetime import datetime, timedelta
import requests


def index_relatorios(request):
    return render(request, 'index_relatorios.html')


def clientes_ativos(request):
    url = "http://127.0.0.1:8000/clientes/"
    response = requests.get(url).json()
    ativos = []
    trinta_dias = datetime.now() - timedelta(days=30)
    
    for cliente in response:
        if datetime.fromisoformat(cliente['atualizado_em']) >= trinta_dias:
            ativos.append(cliente)
            
    return render(request, 'clientes_ativos.html', {'clientes_ativos': ativos})

def novos_registros(request):
    url = "http://127.0.0.1:8000/clientes/"
    response = requests.get(url).json()
    novos = []

    data_inicial = request.GET.get('inicio', '2024-01-01')
    data_final = request.GET.get('fim', str(datetime.now().date()))

    for cliente in response:
        if data_inicial <= cliente['criado_em'] <= data_final:
            novos.append(cliente)

    return render(request, 'novos_registros.html', {'novos_registros': novos})

def produtos_populares(request):
    url = "http://127.0.0.1:8000/inventario/produtos/"
    response = requests.get(url).json()
    populares = sorted(response, key=lambda x: x['alteracoes'], reverse=True)[:5]

    return render(request, 'produtos_populares.html', {'produtos_populares': populares})

def estoque_baixo(request):
    url = "http://127.0.0.1:8000/inventario/produtos/"
    response = requests.get(url).json()
    limite_critico = int(request.GET.get('limite', 10))
    baixos = [produto for produto in response if produto['quantidade'] < limite_critico]

    return render(request, 'estoque_baixo.html', {'estoque_baixo': baixos})

def insights_gerais(request):
    clientes_url = "http://127.0.0.1:8000/clientes/"
    inventario_url = "http://127.0.0.1:8000/inventario/produtos/"

    clientes = requests.get(clientes_url).json()
    produtos = requests.get(inventario_url).json()

    total_clientes = len(clientes)
    novos_clientes = [c for c in clientes if datetime.fromisoformat(c['criado_em']) >= (datetime.now() - timedelta(days=30))]
    percentual_novos = (len(novos_clientes) / total_clientes) * 100 if total_clientes > 0 else 0

    produtos_populares = sorted(produtos, key=lambda x: x['alteracoes'], reverse=True)[:3]
    total_estoque = sum(p['quantidade'] for p in produtos)

    context = {
        'total_clientes': total_clientes,
        'percentual_novos_clientes': percentual_novos,
        'produtos_populares': produtos_populares,
        'total_estoque': total_estoque
    }

    return render(request, 'insights_gerais.html', context)
