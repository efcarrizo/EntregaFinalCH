from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .forms import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth  import login, logout, authenticate

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
    
    
    return render(req, 'ventas.html', {"mensaje": "ventas"})

#########################################################################################

#Forms method post

#Crear un cliente
def clientesformularios(req): 
    if req.method == 'POST': #Si el metodo que se envia es de tipo post entra en este condicional
        
        miFormulario = ClienteFormulario(req.POST) #Se obtiene en una variable ese formulario
        
        if miFormulario.is_valid(): #Si estan todos los campos llenos entra en este condicional
            
            data = miFormulario.cleaned_data  #Recupera todos los datos del formulario en la variable data
            
            nombre = data["nombre"] #Se le asignan valores a cada dato recuperado del formulario
            apellido = data["apellido"]
            email = data["email"]
            
            existing_cliente = Cliente.objects.filter(email=email).first() # Verificar si ya existe un cliente en la base de datos con el mismo email
            
            if existing_cliente: #Si el email del cliente existe entra en este condicional
                return render(req, "inicio.html", {"mensaje": "Ya existe un cliente con este correo electrónico"})
            else:
                cliente = Cliente(nombre=nombre, apellido=apellido, email=email) # Si no existe un cliente con el mismo email, crea uno nuevo
                cliente.save()
                return render(req, "inicio.html", {"mensaje": "Cliente creado con éxito"})
        else:
            return render(req, "inicio.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ClienteFormulario() #Si no entra por metodo post Muestra el formulario vacio
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
    
    cliente = Cliente.objects.get(id=id) #cliente obtiene la id del Modelo cliente
    
    
    if req.method == 'POST': #Si el formulario viene en metodo post
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
    context_object_name = "CreacionDOCURSINHO"
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


#########################################################################################

#Login

def userlogin(req):
    resultado = None
    if req.method == 'POST': #Si el metodo en el que viene la request es post
        
        miFormulario = AuthenticationForm(req, data=req.POST) #El formulario es un form de autenticacion que recbe en la keyword data lo que viene en el formulario
        
        if miFormulario.is_valid(): #Si el formulario es valido entrmaos en este condicional
            
            data = miFormulario.cleaned_data #Data obtiene todos los datos de mi formulario
            usuario = data["username"] 
            pw = data["password"]
            
            user = authenticate(username=usuario, password=pw) #user obtiene el metodo authenticate que pide como dos parametros username que es el usuario que tenemos de la data y password que es el pw que tenemos de la data
            
            if user: #Si el usuario existe entra en este condicional
                login(req, user) #Se llama al metodo login y se le pasa el user
                resultado = render(req, "inicio.html", {"mensaje": f"Bienvenido {user}"})
            else: #Si el usuario no existe entra en este 
                resultado = render(req, "inicio.html", {"mensaje": "Datos incorrectos"})
        else:
            resultado = render(req, "inicio.html", {"mensaje":"Formulario invalido"})
    else:
        miFormulario = AuthenticationForm() #Si entra con un metodo get miFormulario obtiene el formulario de registro de usuario
        resultado = render(req, 'login.html', {"miFormulario": miFormulario}) #Renderiza la pagina de inicio con el contexto del formulario para mostrar
    
    return resultado
        
#Crear usuario

def usercreate(req):
    resultado = None
    if req.method == 'POST': #Si el metodo en el que viene la request es post
        
        miFormulario = UserCreationForm(req.POST) 
        
        if miFormulario.is_valid(): #Si el formulario es valido entramos en este condicional
            
            data = miFormulario.cleaned_data #Data obtiene todos los datos de mi formulario
            
            username = data["username"]
            
            miFormulario.save() #El mismo formulario tiene el metodo save, y lo hace automatico.
            
            resultado = render(req, "inicio.html", {"mensaje": f"Usuario {username} creado con exito!"})
        else:
            resultado = render(req, "inicio.html", {"mensaje":"Formulario invalido"})
                 
    else:
        miFormulario = UserCreationForm() #Si entra con un metodo get miFormulario obtiene el formulario de creacion de usuario vacio
        resultado = render(req, "register.html", {"miFormulario": miFormulario}) #Renderiza la pagina de inicio con el contexto del formulario para mostrar
    
    return resultado