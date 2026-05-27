from django.urls import path
from .views import agenda_por_data, api_calendario

urlpatterns = [
    path('api/', agenda_por_data, name='agenda_api'),
    path('api-calendario/', api_calendario, name='api_calendario' )
]
