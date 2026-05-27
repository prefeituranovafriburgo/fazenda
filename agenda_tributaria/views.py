from datetime import datetime
from django.http import JsonResponse


from calendar import monthrange
from .models import AgendaTributaria


def api_agenda_tributaria(request):
    data_str = request.GET.get("data")

    # Se não passar data -> pega hoje
    if not data_str:
        data_filtro = datetime.today().date()
    else:
        try:
            data_filtro = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse(
                {"erro": "Formato inválido. Use: YYYY-MM-DD"},
                status=400
            )

    registros = AgendaTributaria.objects.filter(data=data_filtro)

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
    data = request.GET.get('data')

    if not data:
        return JsonResponse({'erro': 'Data não informada'}, status=400)

    try:
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'erro': 'Formato inválido. Use YYYY-MM-DD'}, status=400)

    eventos = AgendaTributaria.objects.filter(data=data_obj)

    lista = [{
        'titulo': e.titulo,
        'descricao': e.descricao,
        'data': e.data.strftime('%d de %B de %Y')
    } for e in eventos]

    return JsonResponse(lista, safe=False)


def api_calendario(request):
    mes = int(request.GET.get("mes"))
    ano = int(request.GET.get("ano"))
    import datetime as dt
    primeiro_dia = dt.date(ano, mes, 1)
    dia_semana = primeiro_dia.weekday()  # seg=0
    dia_semana = (dia_semana + 1) % 7    # dom=0

    qtd_dias = monthrange(ano, mes)[1]

    dias_mes = [0] * dia_semana + list(range(1, qtd_dias + 1))

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
