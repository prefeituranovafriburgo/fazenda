import datetime as dt
from django.http import JsonResponse
from calendar import monthrange
from .models import AgendaTributaria 

def api_agenda_tributaria(request):
    """
    API que retorna eventos da `AgendaTributaria` para uma data específica.

    Respostas:
    - 200: JSON com a data consultada, quantidade de registros e lista de registros.
    - 400: JSON com erro quando o formato da data é inválido.
    """
    data_str = request.GET.get("data")

    # Se não passar data -> usa a data de hoje
    if not data_str:
        data_filtro = dt.datetime.today().date()
    else:
        try:
            # Converte string 'YYYY-MM-DD' para `date`
            data_filtro = dt.datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse(
                {"erro": "Formato inválido. Use: YYYY-MM-DD"},
                status=400
            )

    # Recupera todos os registros daquele dia
    registros = AgendaTributaria.objects.filter(data=data_filtro)

    # Serializa os registros para uma estrutura JSON
    resultado = []
    for r in registros:
        resultado.append({
            "id": r.id,
            "titulo": r.titulo,
            "descricao": r.descricao,
            "data": r.data.strftime("%Y-%m-%d")
        })

    return JsonResponse({
        "data": data_filtro.strftime("%Y-%m-%d"),
        "quantidade": registros.count(),
        "registros": resultado
    })


def agenda_por_data(request):
    """
    Endpoint alternativo que retorna os eventos de uma data no formato '10 de Maio de 2021'.

    Retorna lista com objetos contendo `titulo`, `descricao`
    e `data` formatada para leitura humana.
    """
    data = request.GET.get('data')

    if not data:
        return JsonResponse({'erro': 'Data não informada'}, status=400)

    try:
        data_obj = dt.datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'erro': 'Formato inválido. Use YYYY-MM-DD'}, status=400)

    eventos = AgendaTributaria.objects.filter(data=data_obj)

    # Gera uma lista com datas formatadas por extenso
    lista = [{
        'titulo': e.titulo,
        'descricao': e.descricao,
        'data': e.data.strftime('%d de %B de %Y')
    } for e in eventos]

    return JsonResponse(lista, safe=False)


def api_calendario(request):
    """
    Gera os dados necessários para renderizar um calendário mensal.

    Query params esperados:
    - mes: número do mês (1-12)
    - ano: ano (4 dígitos)

    Retorna um JSON contendo:
    - lista `dias_mes` que inclui zeros para os dias vazios no início da semana
    - `dias_com_obrigacao`: lista dos dias do mês que possuem eventos cadastrados
    - nomes e referências para navegação (mês/ano anterior e próximo)
    - `dia_hoje`: dia atual quando o mês/ano consultado corresponder ao atual
    """
    mes = int(request.GET.get("mes"))
    ano = int(request.GET.get("ano"))

    # Primeiro dia do mês (objeto date)
    primeiro_dia = dt.date(ano, mes, 1)
    # weekday(): segunda=0 ... domingo=6. Ajustamos para domingo=0.
    dia_semana = primeiro_dia.weekday()  # seg=0
    dia_semana = (dia_semana + 1) % 7    # dom=0

    # Quantidade de dias no mês
    qtd_dias = monthrange(ano, mes)[1]

    # Lista que representa as células do calendário; '0' indica célula vazia
    dias_mes = [0] * dia_semana + list(range(1, qtd_dias + 1))

    # Dias do mês que tem pelo menos uma obrigação/evento
    dias_com_obrigacao = list(
        AgendaTributaria.objects.filter(
            data__year=ano,
            data__month=mes
        ).values_list("data__day", flat=True).distinct()
    )

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    # Mês/ano anterior e próximo (para navegação)
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1

    mes_proximo = mes + 1 if mes < 12 else 1
    ano_proximo = ano if mes < 12 else ano + 1

    # Indica o dia atual quando o mês/ano solicitado for o mês/ano de hoje
    hoje = dt.date.today()
    dia_hoje = hoje.day if hoje.month == mes and hoje.year == ano else None

    return JsonResponse({
        "mes": mes,
        "ano": ano,
        "mes_nome": meses[mes - 1],
        "dias_mes": dias_mes,
        "dias_com_obrigacao": dias_com_obrigacao,
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior,
        "mes_proximo": mes_proximo,
        "ano_proximo": ano_proximo,
        "dia_hoje": dia_hoje,
    })
