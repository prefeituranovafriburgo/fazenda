from django.urls import path
from .views import api_agenda_tributaria, agenda_por_data, api_calendario

urlpatterns = [
    # path("api/", api_agenda_tributaria, name="api_agenda_tributaria"),
    path('api/', agenda_por_data, name='agenda_api'),
    path('api-calendario/', api_calendario, name='api_calendario' )
]
