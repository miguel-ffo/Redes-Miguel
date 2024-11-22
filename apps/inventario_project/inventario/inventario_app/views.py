from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm
import pymysql
#Lista todos os produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    # Verifica se a requisição deseja os dados em JSON
    if request.GET.get('format') == 'json':
        produtos_data = [{"id": produto.id, "nome": produto.nome, "preco": produto.preco, "descricao": produto.descricao} for produto in produtos]
        return JsonResponse(produtos_data, safe=False)  # Retorna os dados como JSON
    
    # Caso contrário, renderiza a página HTML
    return render(request, 'lista_produtos.html', {'produtos': produtos})

#cria um novo produto
def cria_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'form_produto.html', {'form': form})


#Edita um produto existente
def edita_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request,'form_produto.html', {'form': form})
    
#Deleta um produto
def deleta_produto(request, id):
    produto = get_object_or_404(Produto, id=id)  
    produto.delete()
    return redirect('lista_produtos')       


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
            host='inventario-db',  # Nome do serviço no cliente-network
            user='root',
            password='root',
            database='inventario_db'
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