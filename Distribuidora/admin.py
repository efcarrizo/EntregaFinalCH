from django.contrib import admin
from Distribuidora.models import *

class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'apellido'] #En la pestaña clientes del admin genera un buscador
    
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'stock'] #En el admin se ven las dos categorias al estar dentro del mopdelo
    search_fields = ['nombre', 'categoria']

# Register your models here.
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Avatar)
admin.site.register(Compra)