from django.shortcuts import render
from datetime import datetime, timedelta
import requests
from .models import Cliente
from django.db import connections
import heapq

def index_relatorios(request):
    return render(request, 'index_relatorios.html')

def clientes_ativos(request):
    # Conectando ao banco de dados do cliente
    with connections['cliente'].cursor() as cursor:  # Use o alias configurado para o banco cliente
        # Query para buscar clientes atualizados nos últimos 30 dias
        trinta_dias = datetime.now() - timedelta(days=30)
        query = """
            SELECT id, nome, data_criacao 
            FROM cliente_app_cliente  
            WHERE data_criacao >= %s
        """
        cursor.execute(query, [trinta_dias])
        # Obtendo os resultados
        rows = cursor.fetchall()

    ativos = []
    try:
        # Verifique se os dados são retornados
        for row in cursor.fetchall():
            print(row)  # Isso ajuda a garantir que os dados estão sendo retornados corretamente
            ativos.append({
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'endereco': row[3],
                'telefone': row[4],
                'data_criacao': row[5],
            })
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'clientes_ativos.html', {'clientes_ativos': ativos})

def index_relatorios(request):
    return render(request, 'index_relatorios.html')

def clientes_ativos(request):
    with connections['cliente'].cursor() as cursor:
        trinta_dias = datetime.now() - timedelta(days=30)
        query = """
            SELECT id, nome, data_criacao 
            FROM cliente_app_cliente  
            WHERE data_criacao >= %s
        """
        cursor.execute(query, [trinta_dias])
        rows = cursor.fetchall()

    ativos = []
    try:
        ativos.extend(
            {
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'endereco': row[3],
                'telefone': row[4],
                'data_criacao': row[5],
            }
            for row in rows
        )
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'clientes_ativos.html', {'clientes_ativos': ativos})

def novos_registros(request):
    cursor = connections['cliente'].cursor()

    data_inicial = request.GET.get('inicio', '2024-01-01')
    data_final = request.GET.get('fim', str(datetime.now().date()))

    query = """
        SELECT * FROM cliente_app_cliente
        WHERE data_criacao BETWEEN %s AND %s
    """
    cursor.execute(query, [data_inicial, data_final])

    rows = cursor.fetchall()

    novos = []
    try:
        novos.extend(
            {
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'endereco': row[3],
                'telefone': row[4],
                'data_criacao': row[5],
            }
            for row in rows
        )
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'clientes_ativos.html', {'clientes_ativos': novos})

def produtos_populares(request):
    url = "http://inventario-api:8001/inventario/produtos/"
    response = requests.get(url).json()
    populares = heapq.nlargest(5, response, key=lambda x: x['alteracoes'])

    return render(request, 'produtos_populares.html', {'produtos_populares': populares})

def estoque_baixo(request):
    url = "http://inventario-api:8001/inventario/produtos/"
    response = requests.get(url).json()
    limite_critico = int(request.GET.get('limite', 10))
    baixos = [produto for produto in response if produto['quantidade'] < limite_critico]

    return render(request, 'estoque_baixo.html', {'estoque_baixo': baixos})

def insights_gerais(request):
    clientes_url = "http://cliente-api:8000/api/clientes/"
    inventario_url = "http://inventario-api:8001/inventario/produtos/"

    clientes = requests.get(clientes_url).json()
    produtos = requests.get(inventario_url).json()

    total_clientes = len(clientes)
    novos_clientes = [c for c in clientes if datetime.fromisoformat(c['criado_em']) >= (datetime.now() - timedelta(days=30))]
    percentual_novos = (len(novos_clientes) / total_clientes) * 100 if total_clientes > 0 else 0

    produtos_populares = heapq.nlargest(3, produtos, key=lambda x: x['alteracoes'])
    total_estoque = sum(p['quantidade'] for p in produtos)

    context = {
        'total_clientes': total_clientes,
        'percentual_novos_clientes': percentual_novos,
        'produtos_populares': produtos_populares,
        'total_estoque': total_estoque
    }

    return render(request, 'insights_gerais.html', context)


from django.db import connections

def novos_registros(request):
    cursor = connections['cliente'].cursor()

    data_inicial = request.GET.get('inicio', '2024-01-01')
    data_final = request.GET.get('fim', str(datetime.now().date()))

    query = """
        SELECT * FROM cliente_app_cliente
        WHERE data_criacao BETWEEN %s AND %s
    """
    cursor.execute(query, [data_inicial, data_final])

    rows = cursor.fetchall()

    novos = []
    try:
        # Verifique se os dados são retornados
        for row in cursor.fetchall():
            print(row)  # Isso ajuda a garantir que os dados estão sendo retornados corretamente
            novos.append({
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'endereco': row[3],
                'telefone': row[4],
                'data_criacao': row[5],
            })
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'clientes_ativos.html', {'clientes_ativos': novos})

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

