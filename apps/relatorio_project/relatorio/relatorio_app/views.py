from django.shortcuts import render
from datetime import datetime, timedelta
import requests


def index_relatorios(request):
    return render(request, 'index_relatorios.html')

def clientes_ativos(request):
    url = "http://cliente-api:8000/api/clientes/"  # Alteração: usaremos o nome do serviço cliente-api
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro se o código de status não for 2xx
        response = response.json()
    except requests.exceptions.RequestException as e:
        # Caso ocorra erro na requisição, você pode exibir um erro amigável ou logar a exceção
        print(f"Erro na requisição para clientes: {e}")
        return render(request, 'erro.html', {'error': 'Erro ao buscar clientes'})
    
    ativos = []
    trinta_dias = datetime.now() - timedelta(days=30)
    for cliente in response:
        if datetime.fromisoformat(cliente['atualizado_em']) >= trinta_dias:
            ativos.append(cliente)
    
    return render(request, 'clientes_ativos.html', {'clientes_ativos': ativos})

def novos_registros(request):
    url = "http://cliente-api:8000/api/clientes/"  # Alteração
    response = requests.get(url).json()
    novos = []

    # Converte as strings para objetos datetime
    data_inicial = datetime.strptime(request.GET.get('inicio', '2024-01-01'), '%Y-%m-%d')
    data_final = datetime.strptime(request.GET.get('fim', str(datetime.now().date())), '%Y-%m-%d')

    for cliente in response:
        criado_em = datetime.fromisoformat(cliente['criado_em'])  # Converter o campo 'criado_em' para datetime
        if data_inicial <= criado_em <= data_final:
            novos.append(cliente)

    return render(request, 'novos_registros.html', {'novos_registros': novos})


def produtos_populares(request):
    url = "http://inventario-api:8001/inventario/produtos/"  # Alteração: agora usamos inventario-api
    response = requests.get(url).json()
    populares = sorted(response, key=lambda x: x['alteracoes'], reverse=True)[:5]

    return render(request, 'produtos_populares.html', {'produtos_populares': populares})

def estoque_baixo(request):
    url = "http://inventario-api:8001/inventario/produtos/"  # Alteração
    response = requests.get(url).json()
    limite_critico = int(request.GET.get('limite', 10))
    baixos = [produto for produto in response if produto['quantidade'] < limite_critico]

    return render(request, 'estoque_baixo.html', {'estoque_baixo': baixos})


def insights_gerais(request):
    clientes_url = "http://cliente-api:8000/api/clientes/"  # Alteração
    inventario_url = "http://inventario-api:8001/inventario/produtos/"  # Alteração

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

