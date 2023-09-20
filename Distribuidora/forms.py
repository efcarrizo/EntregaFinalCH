from django import forms

class ClienteFormulario(forms.Form):
    
    nombre = forms.CharField(required=True) #Required significa que es requerido
    apellido = forms.CharField(required=True)
    email = forms.EmailField(required=True)