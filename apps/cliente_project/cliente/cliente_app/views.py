from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
import pymysql

#Listar Clientes
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

def clientes_list_api(request):
    clientes = Cliente.objects.all()
    clientes_data = list(clientes.values())  # Transforma os dados dos clientes em dicionário
    return JsonResponse(clientes_data, safe=False)

#Criar um novo cliente
def cria_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'form_cliente.html', {'form': form})

#Editar um cliente existente
def edita_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'form_cliente.html', {'form': form})

#Deleta um cliente
def deleta_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes')

def executar_query(request):
    query = request.GET.get('query')  # Recebe a query via parâmetro GET
    if not query:
        return JsonResponse({'error': 'Query não fornecida'}, status=400)

    # Evitar consultas perigosas
    palavras_proibidas = ['DROP', 'DELETE', 'ALTER', 'TRUNCATE']
    if any(palavra in query.upper() for palavra in palavras_proibidas):
        return JsonResponse({'error': 'Consulta proibida'}, status=403)

    try:
        # Conectando ao banco de dados cliente-db
        with pymysql.connect(
            host='cliente-db',  # Nome do serviço no cliente-network
            user='root',
            password='root',
            database='cliente_db'
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()  # Pega todos os resultados

                # Formata os resultados como JSON
                colunas = [desc[0] for desc in cursor.description]
                dados = [dict(zip(colunas, row)) for row in result]

        return JsonResponse({'data': dados}, safe=False)
    except pymysql.MySQLError as e:
        return JsonResponse({'error': f'Erro no banco de dados: {str(e)}'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)
