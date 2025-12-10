from django.shortcuts import render
from django.db.models import Q
from .models import Ferramenta


def pesquisa_ferramentas(request):
    query = request.GET.get("q")
    resultados = Ferramenta.objects.all()

    if query:
        palavras = query.split()

        for palavra in palavras:
            resultados = resultados.filter(
                Q(titulo__icontains=palavra) |
                Q(descricao__icontains=palavra)
            )


    context = {
        'query': query,
        'resultados': resultados
    }

    return render(request, 'ferramentas_site/busca_resultados.html', context)

