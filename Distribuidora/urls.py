from django.urls import path
from Distribuidora.views import *

urlpatterns = [
    path('agrega-cliente/<nombre>/<apellido>/<email>', cliente),
    path('lista_clientes/', lista_clientes),
    path('', inicio, name="Inicio"),
    path('clientes/', clientes, name="Clientes"),
    path('productos/', productos, name="Productos"),
    path('ventas/', ventas, name="Ventas" ),
    
]