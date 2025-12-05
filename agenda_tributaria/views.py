from datetime import datetime
from django.http import JsonResponse
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
