from django import forms

class ClienteFormulario(forms.Form):
    
    nombre = forms.CharField(required=True) #Required significa que es requerido
    apellido = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
class ProductoFormulario(forms.Form):
    
    nombre = forms.CharField(required=True) #Required significa que es requerido
    codigo = forms.IntegerField(required=True)
    categoria = forms.CharField(required=True)
    precio = forms.DecimalField(required=True)
    stock = forms.IntegerField(required=True)