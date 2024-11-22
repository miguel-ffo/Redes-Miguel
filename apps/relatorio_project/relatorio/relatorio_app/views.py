from urllib.parse import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import requests
from .models import Cliente
from django.db import connections
import heapq
from urllib.parse import urlencode

def index_relatorios(request):
    return render(request, 'index_relatorios.html')

from datetime import datetime, timedelta
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def clientes_ativos(request):
    # Calculando a data de 30 dias atrás
    trinta_dias = datetime.now() - timedelta(days=30)
    # Formatar a data para o formato esperado no banco (ex: 'YYYY-MM-DD')
    data_formatada = trinta_dias.strftime('%Y-%m-%d')

    # Construir a consulta SQL usando a data formatada
    query = f"SELECT * FROM cliente_app_cliente WHERE data_criacao >= '{data_formatada}'"
    
    # Construir a URL para a API
    url = f"http://cliente-api:8000/executar-query/?query={query}"

    try:
        # Realizando a requisição GET para a API
        response = requests.get(url)

        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON

            # Verificar se existe a chave 'data' no JSON retornado
            if 'data' in data:
                ativo = [
                    {
                        'id': row['id'],
                        'nome': row['nome'],
                        'email': row['email'],
                        'telefone': row['telefone'],
                        'endereco': row['endereco'],
                        'data_criacao': row['data_criacao'],
                    }
                    for row in data['data']
                ]
                # Renderizando a resposta com os dados
                return render(request, 'clientes_ativos.html', {'clientes_ativos': ativo})
            else:
                return HttpResponse("Erro: Dados não encontrados na resposta.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response.status_code}", status=500)

    except requests.ConnectionError:
        return JsonResponse({'error': 'Falha na conexão com cliente-api'}, status=500)
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({'error': f'Erro HTTP: {http_err}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




        # Obtendo os resultados
    


def novos_registros(request):

    data_inicial = request.GET.get('inicio', '2024-01-01')
    data_final = request.GET.get('fim', str(datetime.now().date()))

    query = f"SELECT * FROM cliente_app_cliente WHERE data_criacao BETWEEN '{data_inicial}' AND '{data_final}'"
    
    # Construir a URL para a API
    url = f"http://cliente-api:8000/executar-query/?query={query}"

    try:
        # Realizando a requisição GET para a API
        response = requests.get(url)

        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON

            # Verificar se existe a chave 'data' no JSON retornado
            if 'data' in data:
                novo = [
                    {
                        'id': row['id'],
                        'nome': row['nome'],
                        'email': row['email'],
                        'telefone': row['telefone'],
                        'endereco': row['endereco'],
                        'data_criacao': row['data_criacao'],
                    }
                    for row in data['data']
                ]
                # Renderizando a resposta com os dados
                return render(request, 'novos_registros.html', {'novos_registros': novo})
            else:
                return HttpResponse("Erro: Dados não encontrados na resposta.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response.status_code}", status=500)

    except requests.ConnectionError:
        return JsonResponse({'error': 'Falha na conexão com cliente-api'}, status=500)
    except requests.exceptions.HTTPError as http_err:
        return JsonResponse({'error': f'Erro HTTP: {http_err}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def produtos_populares(request):
    query = "SELECT * FROM inventario_app_produto WHERE quantidade >= 100"
    
    # Codificando a consulta SQL para a URL
    params = {'query': query}
    url = f"http://inventario-api:8001/executar-query/?{urlencode(params)}"

    try:
        # Realizando a requisição GET para a API
        response = requests.get(url)

        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON

            # Verificar se existe a chave 'data' no JSON retornado
            if 'data' in data:
                popular = [
                    {
                        'id': row['id'],
                        'nome': row['nome'],
                        'descricao': row['descricao'],
                        'quantidade': row['quantidade'],
                        'preco': row['preco'],
                        'data_criacao': row['data_criacao'],
                    }
                    for row in data['data']
                ]
                # Renderizando a resposta com os dados
                return render(request, 'produtos_populares.html', {'produtos_populares': popular})
            else:
                return HttpResponse("Erro: Dados não encontrados na resposta.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response.status_code}. Detalhes: {response.text}", status=500)

    except requests.ConnectionError:
        return HttpResponse('Falha na conexão com inventario-api', status=500)
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f'Erro HTTP: {http_err}', status=400)
    except Exception as e:
        return HttpResponse(f'Erro inesperado: {str(e)}', status=500)


def estoque_baixo(request):
    query = "SELECT * FROM inventario_app_produto WHERE quantidade <= 10"
    
    # Codificando a consulta SQL para a URL
    params = {'query': query}
    url = f"http://inventario-api:8001/executar-query/?{urlencode(params)}"

    try:
        # Realizando a requisição GET para a API
        response = requests.get(url)

        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            data = response.json()  # Converte a resposta para JSON

            # Verificar se existe a chave 'data' no JSON retornado
            if 'data' in data:
                baixo = [
                    {
                        'id': row['id'],
                        'nome': row['nome'],
                        'descricao': row['descricao'],
                        'quantidade': row['quantidade'],
                        'preco': row['preco'],
                        'data_criacao': row['data_criacao'],
                    }
                    for row in data['data']
                ]
                # Renderizando a resposta com os dados
                return render(request, 'estoque_baixo.html', {'estoque_baixo': baixo})
            else:
                return HttpResponse("Erro: Dados não encontrados na resposta.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response.status_code}. Detalhes: {response.text}", status=500)

    except requests.ConnectionError:
        return HttpResponse('Falha na conexão com inventario-api', status=500)
    except requests.exceptions.HTTPError as http_err:
        return HttpResponse(f'Erro HTTP: {http_err}', status=400)
    except Exception as e:
        return HttpResponse(f'Erro inesperado: {str(e)}', status=500)


def insights_gerais(request):
    # Consulta para obter todos os clientes
    query_clientes = "SELECT * FROM cliente_app_cliente"
    url_clientes = f"http://cliente-api:8000/executar-query/?query={query_clientes}"

    try:
        # Realizando a requisição GET para a API de clientes
        response_clientes = requests.get(url_clientes)

        if response_clientes.status_code == 200:
            # Converte a resposta para JSON
            data_clientes = response_clientes.json()

            if 'data' in data_clientes:
                clientes = data_clientes['data']
                total_clientes = len(clientes)

                # Filtra os novos clientes criados nos últimos 30 dias
                novos_clientes = []
                for c in clientes:
                    try:
                        # Supondo que a data de criação está no formato ISO
                        data_criacao = datetime.fromisoformat(c['data_criacao'])
                        if data_criacao >= (datetime.now() - timedelta(days=30)):
                            novos_clientes.append(c)
                    except (ValueError, KeyError) as e:
                        print(f"Erro ao processar cliente: {c}, erro: {e}")
            else:
                return HttpResponse("Erro: Dados não encontrados na resposta de clientes.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response_clientes.status_code}", status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Erro ao fazer requisição para cliente-api: {str(e)}'}, status=500)

    # Consulta para obter todos os produtos
    query_produtos = "SELECT * FROM inventario_app_produto"
    url_produtos = f"http://inventario-api:8001/executar-query/?query={query_produtos}"

    try:
        # Realizando a requisição GET para a API de produtos
        response_produtos = requests.get(url_produtos)

        if response_produtos.status_code == 200:
            # Converte a resposta para JSON
            data_produtos = response_produtos.json()

            if 'data' in data_produtos:
                produtos = data_produtos['data']

                # Filtra produtos com quantidade >= 100 e transforma em dicionários
                produtos_populares = [
                    {
                        'id': row['id'],
                        'nome': row['nome'],
                        'descricao': row['descricao'],
                        'quantidade': row['quantidade'],
                        'preco': row['preco'],
                        'data_criacao': row['data_criacao'],
                    }
                    for row in produtos if row['quantidade'] >= 100
                ]

                # Obtendo os 3 produtos mais populares com maior quantidade
                produtos_populares = sorted(produtos_populares, key=lambda x: x['quantidade'], reverse=True)[:3]

                # Calcular o total de estoque de todos os produtos
                total_estoque = sum(p['quantidade'] for p in produtos)

            else:
                return HttpResponse("Erro: Dados não encontrados na resposta de produtos.", status=500)
        else:
            return HttpResponse(f"Erro ao fazer a requisição. Código de status: {response_produtos.status_code}", status=500)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Erro ao fazer requisição para inventario-api: {str(e)}'}, status=500)

    # Preparando o contexto para enviar ao template
    context = {
        'total_clientes': total_clientes,
        'novos_clientes': novos_clientes,
        'produtos_populares': produtos_populares,
        'total_estoque': total_estoque,
    }

    return render(request, 'insights_gerais.html', context)
