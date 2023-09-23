from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

def cliente(req, nombre, apellido, email):
    
    cliente = Cliente(nombre = nombre, apellido = apellido, email = email)
    cliente.save()
    
    return HttpResponse(f"""
        <p>Curso: {cliente.nombre} - Apellido: {cliente.apellido} Email: {cliente.email} agregado!</p>
        """)

def lista_clientes(req):
    
    lista = Cliente.objects.all()
    
    return render(req, 'lista_clientes.html', {'lista_clientes': lista})


#########################################################################################

#Inicio

def inicio(req):
    
    return render(req, 'inicio.html')

#clientes

def clientes(req):
    
    return render(req, 'clientes.html')

#Productos

def productos(req):
    
    return render(req, 'productos.html')

#Ventas

def ventas(req):
    

    cliente_id = 1
    
    cliente = Cliente.objects.get(id = cliente_id) #Entra a la tabla y trae el cliente de la ID que solicita
    ventas = Venta.objects.filter(cliente = cliente) #Entra a la tabla de ventas y trae al Cliente
    
    return render(req, 'ventas.html', {"ventas": ventas})

#########################################################################################

#Forms method post

#Crear un cliente
def clientesformularios(req):
    if req.method == 'POST':
        miFormulario = ClienteFormulario(req.POST)
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            nombre = data["nombre"]
            apellido = data["apellido"]
            email = data["email"]
            
            # Verificar si ya existe un cliente en la base de datos con el mismo email
            existing_cliente = Cliente.objects.filter(email=email).first()
            
            if existing_cliente:
                return render(req, "inicio.html", {"mensaje": "Ya existe un cliente con este correo electrónico"})
            else:
                # Si no existe un cliente con el mismo email, crea uno nuevo
                cliente = Cliente(nombre=nombre, apellido=apellido, email=email)
                cliente.save()
                return render(req, "inicio.html", {"mensaje": "Cliente creado con éxito"})
        else:
            return render(req, "inicio.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ClienteFormulario()
        return render(req, "clientes_formulario.html", {"miFormulario": miFormulario}) #Se le pasa el contexto miFormulario para mostrar en clientes_formulario.html

#Cargar un Producto    
def productosformulario(req):
    if req.method == 'POST':
        miFormulario = ProductoFormulario(req.POST)
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            nombre = data["nombre"]
            codigo = data["codigo"]
            categoria = data["categoria"]
            precio = data["precio"]
            stock = data["stock"]
            
            # Verificar si ya existe un producto en la base de datos con el mismo nombre
            existing_producto = Producto.objects.filter(nombre=nombre).first()
            
            if existing_producto:
                return render(req, "inicio.html", {"mensaje": "Ya existe un producto con este mismo nombre"})
            else:
                # Si no existe un cliente con el mismo email, crea uno nuevo
                producto = Producto(nombre=nombre, codigo=codigo, categoria=categoria, precio=precio, stock=stock)
                producto.save()
                return render(req, "inicio.html", {"mensaje": "Producto creado con éxito"})
        else:
            return render(req, "inicio.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ProductoFormulario()
        return render(req, "productos_formulario.html", {"miFormulario": miFormulario}) #Se le pasa el contexto miFormulario para mostrar en productos_formulario.html


#########################################################################################

#Search method get

#Busqueda de Productos

def productobusqueda(req):
    
    return render(req, "busqueda_producto.html", {"mensaje" : "hola soy un contexto"})

def producto_buscar(req):
    
   if "producto" in req.GET: #Si se envia un producto verifica que el producto exista
        nombre_producto = req.GET["producto"]
        try:
            producto = Producto.objects.get(nombre=nombre_producto)
            return render(req, 'resultado_busqueda_producto.html', {"producto": producto})
        except Producto.DoesNotExist:
            return render(req, 'resultado_busqueda_producto.html', {"mensaje": "No se encuentra el producto"})
        

#Busqueda de clientes

def clientebusqueda(req):
    
    return render(req, "busqueda_cliente.html", {"mensaje" : "En esta seccion puedes buscar un cliente"})

def cliente_buscar(req):
    
   if "apellido" in req.GET: #Si se envia un apellido verifica que el apellido exista
        apellido_cliente = req.GET["apellido"]
        try:
            clientes = Cliente.objects.filter(apellido__icontains=apellido_cliente)
            resultado = render(req, 'resultado_busqueda_cliente.html', {"clientes": clientes})
        except Cliente.DoesNotExist:
            resultado = render(req, 'resultado_busqueda_cliente.html', {"mensaje": "No se encuentra el Cliente"})

        return resultado

        
        
#########################################################################################

#CRUD

#Leer clientes

def leer_clientes(req):
    clientes = Cliente.objects.all()
    
    return render(req, "leer_clientes.html", {"clientes":clientes})

#Eliminar clientes

def eliminar_clientes(req, id):
    
    if req.method == 'POST':
        
        cliente = Cliente.objects.get(id=id)
        cliente.delete()
        
        clientes = Cliente.objects.all()
        return render(req, "leer_clientes.html", {"clientes":clientes})
    
#Editar clientes

def editar_clientes(req, id):
    
    cliente = Cliente.objects.get(id=id)
    
    
    if req.method == 'POST':
        miFormulario = ClienteFormulario(req.POST)
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            cliente.nombre = data["nombre"]
            cliente.apellido = data["apellido"]
            cliente.email = data["email"]
            cliente.save()
            
            return render(req, "inicio.html", {"mensaje": "Cliente modificado"})
        else:
            return render(req, "inicio.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ClienteFormulario(initial={
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "email": cliente.email      
        })
        return render(req, "editar_cliente.html", {"miFormulario": miFormulario, "id": cliente.id}) #Muestra el formulario con el cliente
    
    
#CRUD con clases

class ClienteList(ListView):
    model = Cliente
    template_name = "clientelist.html"
    context_object_name = "clientes"
    
class ClienteDetail(DetailView):
    model = Cliente
    template_name = "clientedetail.html"
    context_object_name = "cliente"
    
class ClienteCreate(CreateView):
    model = Cliente
    template_name = "clientecreate.html"
    fields = ["nombre", "apellido", "email"]
    success_url = "/distribuidora/"

class ClienteUpdate(UpdateView):
    model = Cliente
    template_name = "clienteupdate.html"
    fields = ["__all__"]
    success_url = "/distribuidora/"

class ClienteDelete(DeleteView):
    model = Cliente
    template_name = "clientedelete.html"
    success_url = "/distribuidora/"


