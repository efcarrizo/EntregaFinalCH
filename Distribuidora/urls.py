from django.urls import path
from Distribuidora.views import *
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    #urls paginas
    path('', inicio, name="Inicio"), 
    path('productos/', productos, name="Productos"),  
    path('ventas/', lista_compras, name="Ventas" ), 
    
    #Form Post
    
    #Formulario para agregar productos.
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
    path('clientes/', leer_clientes, name="ListaClientes"), 
    #Eliminar clientes
    path('eliminar-cliente/<int:id>', eliminar_clientes, name="EliminarCliente"),
    #Actualizar Clientes
    path('editar-cliente/<int:id>', editar_clientes, name="EditarCliente"),
    
    #Leer Productos
    path('leer-productos/', leer_productos, name="LeerProductos"),
    #Eliminar Productos
    path('eliminar-producto/<int:id>', eliminar_producto, name="EliminarProducto"),
    #Editar productos
    path('editar-producto/<int:id>', editar_productos, name="EditarProducto"),
    
    
    #CRUD con clases
    path('list-cliente/', ClienteList.as_view(), name="ListaCliente"),
    path('detail-cliente/<pk>', ClienteDetail.as_view(), name="DetalleClientes"),
    path('create-cliente/', ClienteCreate.as_view(), name="CreaCliente"),
    path('upgrade-cliente/<pk>', ClienteUpdate.as_view(), name="ActualizaCliente"),
    path('delete-cliente/<pk>', ClienteDelete.as_view(), name="EliminaCliente"),
    path('create-compra/', CreateCompra.as_view(), name="ComprarPruebaClase" ),

    #LOGIN
    path('login/', userlogin, name="Login"),
    
    #Register user
    path('register/', usercreate, name="UserCreate"),
    
    #Logout
    path('logout/', LogoutView.as_view(template_name = "base_layout.html"), name="Logout"),
    
    #UserUpdate
    path('user-update/', userupdate, name="UserUpdate"),
    
    #AddAvatar
    path('add-avatar/', addAvatar, name="AgregaAvatar"),
    
    #Compras
    path('compras/', ver_compras, name="Compras"),
    
    
    
    #Cards productos #Pueba
    path('productos-prueba/<int:start>', cards_productos, name="CardsProductos"),
    
    #Comprar producto prueba
    path('comprar/<int:producto_id>/', views.hacer_compra, name='hacer_compra'),
    path('compra-exitosa/', compra_exitosa, name="compra_exitosa"),
    
    #About me 
    path('aboutme/', aboutme, name="Aboutme")
    
    
]
