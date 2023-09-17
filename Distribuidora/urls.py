from django.urls import path
from Distribuidora.views import *

urlpatterns = [
    path('agrega-cliente/<nombre>/<apellido>/<email>', cliente),
    path('lista_clientes/', lista_clientes),
    path('', inicio),
    path('clientes/', clientes),
    path('productos/', productos),
    path('ventas/', ventas),
    
]