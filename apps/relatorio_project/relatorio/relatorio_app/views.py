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
    cursor = connections['cliente'].cursor() # Use o alias configurado para o banco cliente
        # Query para buscar clientes atualizados nos últimos 30 dias
    trinta_dias = datetime.now() - timedelta(days=30)
    query = """
        SELECT * FROM cliente_app_cliente  
        WHERE data_criacao >= %s
    """
    cursor.execute(query, [trinta_dias])

        # Obtendo os resultados
    rows = cursor.fetchall()

    ativos = []
    try:
        # Verifique se os dados são retornados
        for row in rows:  # Use 'rows' que já contém os resultados
            print(row)  # Isso ajuda a garantir que os dados estão sendo retornados corretamente
            ativos.append({
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'telefone': row[3],
                'endereco': row[4],
                'data_criacao': row[5],  # Corrigido para incluir apenas as colunas retornadas
            })
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
                'telefone': row[3],
                'endereco': row[4],
                'data_criacao': row[5],
            }
            for row in rows
        )
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'novos_registros.html', {'novos_registros': novos})

def produtos_populares(request):
    cursor = connections['inventario'].cursor()  # Use o alias configurado para o banco cliente

    # Query para buscar produtos com estoque maior ou igual a 100
    query = """
        SELECT * FROM inventario_app_produto  
        WHERE quantidade >= %s
    """
    cursor.execute(query, [100])  # Filtrando produtos com quantidade >= 100

    # Obtendo os resultados
    rows = cursor.fetchall()

    populares = []
    try:
        # Verifique se os dados são retornados
        for row in rows:  # Use 'rows' que já contém os resultados
            print(row)  # Isso ajuda a garantir que os dados estão sendo retornados corretamente
            populares.append({
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'quantidade': row[3],
                'preco': row[4],
                'data_criacao': row[5],  # Corrigido para incluir apenas as colunas retornadas
            })
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'produtos_populares.html', {'produtos_populares': populares})


def estoque_baixo(request):
    cursor = connections['inventario'].cursor()  # Use o alias configurado para o banco cliente

    # Query para buscar produtos com estoque maior ou igual a 100
    query = """
        SELECT * FROM inventario_app_produto  
        WHERE quantidade <= %s
    """
    cursor.execute(query, [10])  # Filtrando produtos com quantidade >= 100

    # Obtendo os resultados
    rows = cursor.fetchall()

    baixo = []
    try:
        # Verifique se os dados são retornados
        for row in rows:  # Use 'rows' que já contém os resultados
            print(row)  # Isso ajuda a garantir que os dados estão sendo retornados corretamente
            baixo.append({
                'id': row[0],
                'nome': row[1],
                'descricao': row[2],
                'quantidade': row[3],
                'preco': row[4],
                'data_criacao': row[5],  # Corrigido para incluir apenas as colunas retornadas
            })
    except Exception as e:
        print(f"Erro na consulta: {e}")

    return render(request, 'estoque_baixo.html', {'estoque_baixo': baixo})

def insights_gerais(request):
    # Conectando ao banco de dados
    with connections['cliente'].cursor() as cursor:
        # Query para buscar todos os clientes
        cursor.execute("SELECT * FROM cliente_app_cliente")
        clientes = cursor.fetchall()

    total_clientes = len(clientes)
    novos_clientes = []
    for c in clientes:
        try:
            # Supondo que a data de criação está na terceira coluna
            data_criacao = datetime.fromisoformat(c[2])  # Ajuste o índice conforme necessário
            if data_criacao >= (datetime.now() - timedelta(days=30)):
                novos_clientes.append(c)
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar cliente: {c}, erro: {e}")

    percentual_novos = (len(novos_clientes) / total_clientes) * 100 if total_clientes > 0 else 0

    # Buscando produtos do banco de dados
    with connections['inventario'].cursor() as cursor:
        cursor.execute("SELECT * FROM inventario_app_produto")
        produtos = cursor.fetchall()

    # Filtrando produtos com quantidade >= 100 e transformando em dicionários
    produtos_populares = [
        {
            'id': row[0],  # Supondo que o ID está na primeira coluna
            'nome': row[1],  # Supondo que o nome está na segunda coluna
            'descricao': row[2],  # Supondo que a descrição está na terceira coluna
            'quantidade': row[3],  # Supondo que a quantidade está na quarta coluna
            'preco': row[4],  # Supondo que o preço está na quinta coluna
            'data_criacao': row[5],  # Supondo que a data de criação está na sexta coluna
        }
        for row in produtos if row[3] >= 100  # Filtrando produtos com quantidade >= 100
    ]

    # Obtendo os 3 produtos mais populares com maior quantidade
    produtos_populares = heapq.nlargest(3, produtos_populares, key=lambda x: x['quantidade'])

    total_estoque = sum(p['quantidade'] for p in produtos_populares)

    context = {
        'total_clientes': total_clientes,
        'produtos_populares': produtos_populares,
        'total_estoque': total_estoque
    }

    return render(request, 'insights_gerais.html', context)

