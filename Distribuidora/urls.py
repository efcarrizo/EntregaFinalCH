from django.urls import path
from Distribuidora.views import *

urlpatterns = [
    #urls paginas
    path('agrega-cliente/<nombre>/<apellido>/<email>', cliente),
    path('lista_clientes/', lista_clientes),
    path('', inicio, name="Inicio"),
    path('clientes/', clientes, name="Clientes"),
    path('productos/', productos, name="Productos"),
    path('ventas/', ventas, name="Ventas" ),
    
    #Form Post
    
    #Formulario para agregar clientes y productos.
    path('clientes-formulario/', clientesformularios, name="ClientesFormulario"),
    path('productos-formulario/', productosformulario, name="ProductosFormulario"),
    
    #Form Get
    
    #Busqueda de producto, pagina de form y pagina de resultados.
    path('producto-busqueda/', productobusqueda, name="ProductoBusqueda"),
    path('producto-buscar/', producto_buscar, name="ProductoBuscar"),
    
    #Busqueda de Clientes, pagina de forms y pagina de resultados.
    path('cliente-busqueda/', clientebusqueda, name="ClienteBusqueda"),
    path('cliente-buscar/', cliente_buscar, name="ClienteBuscar"),
    
]