from django.shortcuts import render, get_object_or_404
from .models import Servico, PaginasRelacionadas, AcessoRapido, SiteConfiguracao, LinkRodape, NoticiasFazenda, Classe_Formulario, Formularios
import calendar
from datetime import date, datetime
from agenda_tributaria.models import AgendaTributaria
from django.apps import apps

# Create your views here.

MESES_PT_BR = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}

def index(request):
  
    hoje = date.today()

    # parâmetros do mês/ano
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))
    dia_selecionado = int(request.GET.get('dia', hoje.day))

    # Gera calendário
    cal = calendar.Calendar(calendar.SUNDAY)
    dias_mes = list(cal.itermonthdays(ano, mes))

    # Datas de navegação
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1
    mes_proximo = mes + 1 if mes < 12 else 1
    ano_proximo = ano if mes < 12 else ano + 1

    # Data selecionada
    data_selecionada = date(ano, mes, dia_selecionado)

    # Obrigações do dia
    obrigacoes = AgendaTributaria.objects.filter(data=data_selecionada)
    
    context = {
        'titulo': 'Fazenda',
        
        'servicos': Servico.objects.filter(ativo=True),
        'noticias': NoticiasFazenda.objects.filter(ativa=True).order_by('-dt_inclusao'),
        'noticias_destaque': NoticiasFazenda.objects.filter(ativa=True, destaque=True).order_by('ordem_carrossel'),

        'ano': ano,
        "ano_atual": datetime.now().year,
        'mes': mes,  
        'mes_nome': MESES_PT_BR[mes],
        'dias_mes': dias_mes,
        'dia_selecionado': dia_selecionado,
        'obrigacoes': obrigacoes,
        'data_selecionada': data_selecionada,

        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
        "paginas_relacionadas": PaginasRelacionadas.objects.all(),
        'acessos_rapidos': AcessoRapido.objects.all(),
        
    }


    return render(request, 'financas/index.html', context)

def nfse(request):
    context = {

    }
    return render(request, 'financas/nfse.html', context)

def dte(request):
    context = {
        'titulo': 'Domicílio Tributário Eletrônico',
    }
    return render(request, 'financas/dte.html', context)

def cadastramento(request):
    context = {
        'titulo': 'Passo a passo: Cadastramento no Emissor Nacional',
    }
    return render(request, 'financas/cadastramento.html', context)

def noticia_detalhe(request, slug):
    """Exibe o detalhe de uma notícia"""
    noticia = get_object_or_404(NoticiasFazenda, slug=slug, ativa=True)
    
    # Incrementa visualizações
    noticia.incrementar_visualizacoes()
    
    # Obter todas as notícias ativas ordenadas por data (mais recentes primeiro)
    todas_noticias = NoticiasFazenda.objects.filter(ativa=True).order_by('-dt_inclusao')
    noticias_list = list(todas_noticias)
    
    # Encontrar índice da notícia atual
    indice_atual = None
    for i, n in enumerate(noticias_list):
        if n.id == noticia.id:
            indice_atual = i
            break
    
    # Próxima notícia (índice anterior, pois está ordenada por data DESC)
    proxima_noticia = noticias_list[indice_atual - 1] if indice_atual is not None and indice_atual > 0 else None
    
    # Notícia anterior (índice posterior)
    noticia_anterior = noticias_list[indice_atual + 1] if indice_atual is not None and indice_atual < len(noticias_list) - 1 else None
    
    context = {
        'noticia': noticia,
        'proxima_noticia': proxima_noticia,
        'noticia_anterior': noticia_anterior,
    }
    return render(request, 'financas/noticia_detalhe.html', context)


def noticias_lista(request):
    """Lista todas as notícias ativas"""
    noticias = NoticiasFazenda.objects.filter(ativa=True).order_by('-dt_inclusao')
    
    context = {
        'noticias': noticias,
    }
    return render(request, 'financas/noticias_lista.html', context)

def formularios(request):
    classes = Classe_Formulario.objects.all()
    
    context = {
        'classes': classes,
    }
    return render(request, 'financas/formularios.html', context)