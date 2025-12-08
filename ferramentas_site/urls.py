from django.urls import path
from .views import pesquisa_ferramentas

urlpatterns = [
    path('pesquisar/', pesquisa_ferramentas, name='pesquisa_ferramentas'),
]
