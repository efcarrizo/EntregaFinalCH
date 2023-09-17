from django.db import models

class Cliente(models.Model):
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    
    nombre = models.CharField(max_length=100)
    codigo = models.IntegerField()
    categoria = models.CharField(max_length=50) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_venta = models.DateTimeField(auto_now_add=True)
    confirmada = models.BooleanField(default=False)
        
    def __str__(self):
        return 'Productos'