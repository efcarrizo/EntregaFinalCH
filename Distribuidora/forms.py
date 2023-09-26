from django import forms
from .models import *

# class ClienteFormulario(forms.Form):
    
#     nombre = forms.CharField(required=True) #Required significa que es requerido
#     apellido = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
    
class ClienteFormulario(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = ('__all__')

    
class ProductoFormulario(forms.Form):
    
    nombre = forms.CharField(required=True) #Required significa que es requerido
    codigo = forms.IntegerField(required=True)
    categoria = forms.CharField(required=True)
    precio = forms.DecimalField(required=True)
    stock = forms.IntegerField(required=True)