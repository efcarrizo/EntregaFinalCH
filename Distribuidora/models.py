from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    
    def __str__(self):
        return f'{self.apellido} {self.nombre}'
    
class Producto(models.Model):
    
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()
    categoria = models.CharField(max_length=50) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos-img/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.nombre} {self.categoria}'


class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Compra de {self.cantidad} {self.producto.nombre} por {self.cliente.nombre}'

    
class Avatar(models.Model): #Vamos a crear el modelo avatar que tendra 2 campos
    
    #Este campo vincula con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Si se elimina el usuario eliminamos los avatars de ese usuario
    #Este campo es para subir la imagen
    image = models.ImageField(upload_to='avatares/', blank=True, null=True)
        
    def __str__(self):
        return f"{self.user} - {self.image}"
    
   

    