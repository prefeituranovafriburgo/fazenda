from django.contrib import admin
from .models import Servico, PaginasRelacionadas


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem")
    list_editable = ("ativo", "ordem")
    search_fields = ("titulo", "descricao")

@admin.register(PaginasRelacionadas)
class PaginasRelacionadasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link')
from django.contrib import admin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'dt_inclusao', 'ativa', 'visualizacoes']
    list_filter = ['ativa']
    search_fields = ['titulo', 'resumo', 'corpo_da_noticia', 'dt_inclusao']
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'dt_inclusao'
    readonly_fields = ['visualizacoes', 'dt_inclusao', 'dt_atualizacao']
    
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('titulo', 'slug', 'resumo', 'autor')
        }),
        ('Conteúdo', {
            'fields': ('corpo_da_noticia', 'links_uteis')
        }),
        ('Imagens', {
            'fields': ('banner_pequeno', 'banner_carrossel')
        }),
        ('Visibilidade', {
            'fields': ('ativa', 'destaque', 'ordem_carrossel')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes', 'dt_inclusao', 'dt_atualizacao'),
            'classes': ('collapse',)
        }),
    )
