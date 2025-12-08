from datetime import datetime
from .models import SiteConfiguracao, LinkRodape

plataformas = LinkRodape.objects.filter(
        ativo=True,
        tipo='PLATAFORMA'
    ).order_by('ordem')

sistemas = LinkRodape.objects.filter(
    ativo=True,
    tipo='SISTEMA'
).order_by('ordem')

config, created = SiteConfiguracao.objects.get_or_create(pk=1)

def site_config(request):

    
    return {
        'site_config': config,
        'ano_atual': datetime.now().year,
        "links_plataformas": plataformas,
        "links_sistemas": sistemas
    }
