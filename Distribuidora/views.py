from django.shortcuts import render
from .models import *
from django.http import HttpResponse

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
    
    return render(req, 'ventas.html')

#########################################################################################
    