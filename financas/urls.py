from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
 
app_name='financas'
urlpatterns = [
    path('', views.index, name='home'),    
    path('noticia/<slug:slug>/', views.noticia_detalhe, name='noticia_detalhe'),
    path('noticias/', views.noticias_lista, name='noticias_lista'),
    
    path('nfs-e/', views.nfse, name='nfse'),     
    path('dte/', views.dte, name='dte'),     
    path('formularios/', views.formularios, name='formularios'),
    path('cadastramento/', views.cadastramento, name='cadastramento'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
