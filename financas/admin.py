from django.contrib import admin
from .models import Servico, PaginasRelacionadas, AcessoRapido,SiteConfiguracao, LinkRodape, Classe_Formulario, Formularios


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem")
    list_editable = ("ativo", "ordem")
    search_fields = ("titulo", "descricao")

@admin.register(PaginasRelacionadas)
class PaginasRelacionadasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link')
    


from django.contrib import admin
from .models import NoticiasFazenda as Noticia

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'dt_inclusao', 'ativa', 'visualizacoes']
    list_filter = ['ativa']
    search_fields = ['titulo', 'resumo', 'corpo_da_noticia', 'dt_inclusao']
    readonly_fields = ['visualizacoes', 'dt_inclusao', 'dt_atualizacao']


    fieldsets = (
        ('Informações Principais', {
            'fields': ('titulo', 'resumo', 'autor')
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


@admin.register(AcessoRapido)
class AcessoRapidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link', 'icone')
    search_fields = ('titulo',)



@admin.register(SiteConfiguracao)
class SiteConfiguracaoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Não permite adicionar mais de um registro
        if SiteConfiguracao.objects.exists():
            return False
        return True

@admin.register(LinkRodape)
class LinkRodapeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "url", "tipo", "ordem", "ativo", "abrir_em_nova_aba")
    list_editable = ("ordem", "ativo", "abrir_em_nova_aba")
    search_fields = ("titulo",)
    list_filter = ("ativo", "abrir_em_nova_aba")
    ordering = ("ordem",)

@admin.register(Classe_Formulario)
class ClasseFormularioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'div_id', 'dt_inclusao')
    search_fields = ('nome', 'div_id')
    list_filter = ('dt_inclusao',)

@admin.register(Formularios)
class FormulariosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'classe', 'dt_inclusao')
    search_fields = ('titulo', 'classe__nome')
    list_filter = ('dt_inclusao',)
