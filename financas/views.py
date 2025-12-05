from django.shortcuts import render
from .models import Servico, PaginasRelacionadas
import calendar
from datetime import date, datetime
from agenda_tributaria.models import AgendaTributaria
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

        'ano': ano,
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
    }


    return render(request, 'financas/index.html', context)

def nfse(request):
    context = {

    }
    return render(request, 'financas/nfse.html', context)
