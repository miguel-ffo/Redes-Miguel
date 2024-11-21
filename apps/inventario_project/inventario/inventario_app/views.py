from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm

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


