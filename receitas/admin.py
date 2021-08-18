from django.contrib import admin
from .models import Receita

class ListingRecipes(admin.ModelAdmin):
  list_display = (
    'id',
    'nome_receita',
    'categoria',
    'tempo_preparo',
    'rendimento',
    'publicada',
  )

  list_display_links = (
    'id',
    'nome_receita'
  )

  list_filter = ('categoria', 'tempo_preparo')

  list_editable = ('publicada', )

  search_fields = ('nome_receita', )

admin.site.register(Receita, ListingRecipes)
