from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth  import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



#404 si no encuentra una pagina
def error_404(request, exception):
    return render(request, '404.html', status=404)

def lista_productos(req):
    
    lista = Producto.objects.all()
    
    return render(req, 'productos.html', {'lista_productos': lista})


#########################################################################################

#Inicio
def inicio(req):
    
    try:
        avatar = Avatar.objects.get(user = req.user.id)
        return render(req, 'base_layout.html', {"url" : avatar.image.url, "mensaje": "Bienvenid@ a la tienda digital de Annie's Grow"})
    except:
        return render(req, 'base_layout.html')
    
    

#clientes

def clientes(req):
    
    return render(req, 'clientes.html')

#Productos
@login_required
def productos(req):
    productos = Producto.objects.all()
    
    return render(req, "leer_productos.html", {"productos":productos})

#Ventas

def lista_compras(req):
    
    ventas = Compra.objects.all()
    
    return render(req, 'ventas.html', {"ventas": ventas})

#########################################################################################

#Forms method post

#Cargar un Producto
@login_required    
def productosformulario(req):
    if req.method == 'POST':
        miFormulario = ProductoFormulario(req.POST, req.FILES) #Si se suben imagenes hay que poner un req.FILES para poder hacerlo
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            nombre = data["nombre"]
            codigo = data["codigo"]
            categoria = data["categoria"]
            precio = data["precio"]
            stock = data["stock"]
            imagen = data["imagen"]
            
            # Verificar si ya existe un producto en la base de datos con el mismo nombre
            existing_producto = Producto.objects.filter(nombre=nombre).first()
            
            if existing_producto:
                return render(req, "base_layout.html", {"mensaje": "Ya existe un producto con este mismo nombre"})
            else:
                # Si no existe un cliente con el mismo email, crea uno nuevo
                producto = Producto(nombre=nombre, codigo=codigo, categoria=categoria, precio=precio, stock=stock, imagen=imagen)
                producto.save()
                return render(req, "base_layout.html", {"mensaje": "Producto creado con éxito"})
        else:
            return render(req, "base_layout.html", {"mensaje": "Formulario inválido"})

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
            productos = Producto.objects.filter(nombre__icontains=nombre_producto)
            return render(req, 'resultado_busqueda_producto.html', {"productos": productos})
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
            
            return render(req, "base_layout.html", {"mensaje": "Cliente modificado"})
        else:
            return render(req, "base_layout.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ClienteFormulario(initial={
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "email": cliente.email      
        })
        return render(req, "editar_cliente.html", {"miFormulario": miFormulario, "id": cliente.id}) #Muestra el formulario con el cliente

#Leer productos
def leer_productos(req):
    productos = Producto.objects.all()
    
    return render(req, "leer_productos.html", {"productos":productos})

#Eliminar producto
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == 'POST':
        # Si se envió una solicitud POST, significa que el usuario confirmó la eliminación.
        producto.delete()
        return redirect("leer-productos")  # Redirige a la página de destino después de la eliminación

    return render(request, "confirmar_eliminar_producto.html", {"producto": producto})

#Editar productos

def editar_productos(req, id):
    
    producto = Producto.objects.get(id=id) #Producto obtiene la id del Modelo Producto
    
    
    if req.method == 'POST': #Si el formulario viene en metodo post
        miFormulario = ProductoFormulario(req.POST)
        
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            producto.nombre = data["nombre"]
            producto.codigo = data["codigo"]
            producto.categoria = data["categoria"]
            producto.precio = data["precio"]
            producto.stock = data["stock"]
            producto.save()
            
            return render(req, "base_layout.html", {"mensaje": "Producto modificado"})
        else:
            return render(req, "base_layout.html", {"mensaje": "Formulario inválido"})

    else:
        miFormulario = ProductoFormulario(initial={
            "nombre": producto.nombre,
            "codigo": producto.codigo,
            "categoria": producto.categoria,
            "precio": producto.precio,
            "stock": producto.stock,
                  
        })
        return render(req, "editar_producto.html", {"miFormulario": miFormulario, "id": producto.id}) #Muestra el formulario con los datos actuales del producto
    
      
#CRUD con clases

class ClienteList(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "clientelist.html"
    context_object_name = "clientes"
    
class ClienteDetail(DetailView):
    model = Cliente
    template_name = "clientedetail.html"
    context_object_name = "cliente"
    
class ClienteCreate(CreateView):
    model = Cliente
    context_object_name = "CreacionCliente"
    template_name = "clientecreate.html"
    fields = ["nombre", "apellido", "email"]
    success_url = "/distribuidora/"

    def form_valid(self, form):
            # Verificar si el usuario ya tiene un cliente vinculado
            if Cliente.objects.filter(user=self.request.user).exists():
                # Si es así, agregar un error al formulario y devolverlo
                form.add_error(None, "Este usuario ya tiene un cliente vinculado.")
                return self.form_invalid(form)

            # Si no, proceder como antes
            form.instance.user = self.request.user
            return super().form_valid(form)

class ClienteUpdate(UpdateView):
    model = Cliente
    template_name = "clienteupdate.html"
    fields = "__all__"
    success_url = "/distribuidora/"

class ClienteDelete(DeleteView):
    model = Cliente
    template_name = "clientedelete.html"
    success_url = "/distribuidora/"

class CreateCompra(CreateView):
    model = Compra
    fields = ['cliente', 'producto', 'cantidad']
    template_name = "pruebadecompra.html"
    success_url = "/distribuidora/"

    def form_valid(self, form):
        # Obtenemos el producto y la cantidad del formulario
        producto_id = form.cleaned_data['producto'].id
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad_compra = form.cleaned_data['cantidad']

        if cantidad_compra <= 0:
            # Si la cantidad de compra es igual o menor que cero, muestra un mensaje de error
            form.add_error('cantidad', 'La cantidad debe ser mayor que cero.')
            return super().form_invalid(form)

        if cantidad_compra > producto.stock:
            # Si la cantidad de compra es mayor que el stock, muestra un mensaje de error
            form.add_error('cantidad', 'No hay suficiente stock para esta compra.')
            return super().form_invalid(form)

        # La cantidad de compra es válida, así que procedemos a guardar la compra
        response = super().form_valid(form)

        # Actualizamos el stock del producto
        producto.stock -= cantidad_compra
        producto.save()

        return response



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
                resultado = render(req, "base_layout.html", {"mensaje": f"Bienvenido {user}"})
            else: #Si el usuario no existe entra en este 
                resultado = render(req, "base_layout.html", {"mensaje": "Datos incorrectos"})
        else:
            resultado = render(req, "base_layout.html", {"mensaje":"Formulario invalido"})
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
            
            resultado = render(req, "base_layout.html", {"mensaje": f"Usuario {username} creado con exito!"})
        else:
            resultado = render(req, "base_layout.html", {"mensaje":"Formulario invalido"})
                 
    else:
        miFormulario = UserCreationForm() #Si entra con un metodo get miFormulario obtiene el formulario de creacion de usuario vacio
        resultado = render(req, "register.html", {"miFormulario": miFormulario}) #Renderiza la pagina de inicio con el contexto del formulario para mostrar
    
    return resultado

#Editar usuario

def userupdate(req):
    
    user = req.user
    
    if req.method == 'POST':
        
        miFormulario = UserEditForm(req.POST, instance= req.user)
        
        if miFormulario.is_valid():
            
            data = miFormulario.cleaned_data
            
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.email = data["email"]
            user.set_password(data["password1"])
            user.save()
            
            resultado = render(req, "base_layout.html", {"mensaje": "Perfil actualizado con exito"})
        else:
            resultado = render(req, "userupdate.html", {"miFormulario": miFormulario}) #Si def clean_password no valida bien tira el error en este campo
    else:
        miFormulario = UserEditForm(instance = req.user)
        
        resultado = render(req, "userupdate.html", {"miFormulario": miFormulario})
    
    return resultado


#########################################################################################


#Avatar
@login_required
def addAvatar(req):
    if req.method == 'POST':
        miFormulario = AvatarFormulario(req.POST, req.FILES)
        
        if miFormulario.is_valid():
            user = req.user
            existing_avatar = Avatar.objects.filter(user=user).first()
            
            if existing_avatar:
                # Si el usuario ya tiene un avatar, lo rempleaza
                existing_avatar.image = miFormulario.cleaned_data["image"]
                existing_avatar.save()
            else:
                # Si el usuario no tiene un avatar, crea uno nuevo
                avatar = Avatar(user=user, image=miFormulario.cleaned_data["image"])
                avatar.save()
            
            return render(req, "addavatar.html", {"mensaje": "Avatar modificado con exito!"})
    else:
        miFormulario = AvatarFormulario()
    
    return render(req, "addavatar.html", {"miFormulario": miFormulario})

##################################################################################

#Prueba de compra
def hacer_compra(request, producto_id):
    # Obtener el producto que se va a comprar
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = CompraProductoForm(request.POST)

        if form.is_valid():
            cantidad_compra = form.cleaned_data['cantidad']

            # Verificar si hay suficiente stock para la compra
            if cantidad_compra > 0 and producto.stock >= cantidad_compra:
                # Crear una instancia de Compra y guardarla en la base de datos
                compra = Compra(producto=producto, cliente=request.user.cliente, cantidad=cantidad_compra)
                compra.save()

                # Actualizar el stock del producto
                producto.stock -= cantidad_compra
                producto.save()
                
                print(f'Cantidad de compra: {cantidad_compra}')
                print(f'Stock antes de la compra: {producto.stock}')

                # Redirigir a una página de éxito de compra
                return redirect('compra_exitosa')

    else:
        form = CompraProductoForm()

    return render(request, 'hacer_compra.html', {'producto': producto, 'form': form})

def compra_exitosa(req):
    return render(req, 'compra_exitosa.html')


########################################################################################

def cards_productos(req, start=1):
    cant_por_pagina = 3

    start = int(start)

    if req.GET.get("direction") == 'next':
        start += 1
    elif req.GET.get("direction") == 'before':
        start -= 1
    if start <= 0:
        start = 1

    inicio = (start - 1) * cant_por_pagina
    final = start * cant_por_pagina

    productos = Producto.objects.all()[inicio:final]

    # Verifica si hay más productos disponibles
    no_more_products = len(productos) == 0

    return render(req, "cards_productos.html", {"productos": productos, "current_page": start, "no_more_products": no_more_products})



