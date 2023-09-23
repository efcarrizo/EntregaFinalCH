from django.urls import path
from Distribuidora.views import *

urlpatterns = [
    #urls paginas
    path('agrega-cliente/<nombre>/<apellido>/<email>', cliente),
    path('lista_clientes/', lista_clientes),
    path('', inicio, name="Inicio"),
    path('clientes/', leer_clientes, name="Clientes"),
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
    
    #CRUD
    
    #Leer clientes
    path('leer-clientes/', leer_clientes, name="LeerClientes"),
    #Borrar clientes
    path('eliminar-cliente/<int:id>', eliminar_clientes, name="EliminarCliente"),
    #Actualizar archivos
    path('editar-cliente/<int:id>', editar_clientes, name="EditarCliente"),
    
    #CRUD con clases
    path('list-cliente/', ClienteList.as_view(), name="ListaCliente"),
    path('detail-cliente/<pk>', ClienteDetail.as_view(), name="DetalleClientes"),
    path('create-cliente/', ClienteCreate.as_view(), name="CreaCliente"),
    path('upgrade-cliente/<pk>', ClienteUpdate.as_view(), name="ActualizaCliente"),
    path('delete-cliente/<pk>', ClienteDelete.as_view(), name="EliminaCliente"),

    
]