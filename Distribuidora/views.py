from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .forms import *

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
            return render(req, 'resultadoBusqueda.html', {"producto": producto})
        except Producto.DoesNotExist:
            return render(req, 'resultadoBusqueda.html', {"mensaje": "No se encuentra el producto"})
        

#Busqueda de clientes

def clientebusqueda(req):
    
    return render(req, "busqueda_cliente.html", {"mensaje" : "hola soy un contexto"})

def cliente_buscar(req):
    
   if "apellido" in req.GET: #Si se envia un producto verifica que el producto exista
        apellido_cliente = req.GET["apellido"]
        try:
            cliente = Cliente.objects.get(apellido=apellido_cliente)
            return render(req, 'resultadoBusqueda2.html', {"cliente": cliente})
        except Cliente.DoesNotExist:
            return render(req, 'resultadoBusqueda2.html', {"mensaje": "No se encuentra el producto"})


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        