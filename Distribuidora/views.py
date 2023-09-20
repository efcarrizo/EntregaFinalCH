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

#Formularios

# def clientesformularios(req):
#     # print('method', req.method) #Muestra en la terminal el metodo que se uso
#     # print('post', req.POST)#Muestra por consola lo que se mando como post
#     if req.method == 'POST':
        
#         miFormulario = ClienteFormulario(req.POST)
        
#         if miFormulario.is_valid():
            
#             data = miFormulario.cleaned_data
            
#             cliente = Cliente(nombre=data["nombre"], apellido=data["apellido"], email=data["email"])
#             cliente.save()
#             return render(req, "inicio.html", {"mensaje": "Cliente creado con exito"})
#         else:
#             return render(req, "inicio.html", {"mensaje": "Formulario invalido"})

#     else:
#         miFormulario = ClienteFormulario()
#         return render(req, "clientes_formulario.html", {"miFormulario": miFormulario})

from .models import Cliente  # Asegúrate de importar el modelo de Cliente

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
        return render(req, "clientes_formulario.html", {"miFormulario": miFormulario})
