# admin.py
from django.contrib import admin
from .models import Ferramenta

@admin.register(Ferramenta)
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link', 'ativo')
    search_fields = ('titulo', 'descricao')
    list_filter = ('ativo',)
