from django.contrib import admin
from .models import AgendaTributaria


@admin.register(AgendaTributaria)
class AgendaTributariaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')
    list_filter = ('data',)
    search_fields = ('titulo', 'descricao')
    ordering = ('data',)
    date_hierarchy = 'data'

    fieldsets = (
        ("Informações da obrigação", {
            "fields": ("titulo", "descricao")
        }),
        ("Data de vencimento", {
            "fields": ("data",)
        }),
    )
