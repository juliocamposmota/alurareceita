from django.shortcuts import get_object_or_404, render
from .models import Receita

def index(request):
  recipes = Receita.objects.order_by('-date_receita').filter(publicada = True)

  data = {
    'receitas': recipes,
  }

  return render(request, 'index.html', data)

def receita(request, receita_id):
  receita = get_object_or_404(Receita, pk = receita_id)

  recipe_displayed = {
    'receita': receita,
  }

  return render(request, 'receita.html', recipe_displayed)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas' : lista_receitas
    }

    return render(request, 'buscar.html', dados)
