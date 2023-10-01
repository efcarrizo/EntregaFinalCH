from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from django import forms
from .models import *

# class ClienteFormulario(forms.Form):
    
#     nombre = forms.CharField(required=True) #Required significa que es requerido
#     apellido = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
    
class ClienteFormulario(forms.ModelForm):
    
    class Meta: #Se usa para decir a que modelo esta vinculado
        model = Cliente
        fields = ('__all__')

    
class ProductoFormulario(forms.Form):
    
    nombre = forms.CharField(required=True) #Required significa que es requerido
    codigo = forms.IntegerField(required=True)
    categoria = forms.CharField(required=True)
    precio = forms.DecimalField(required=True)
    stock = forms.IntegerField(required=True)
    imagen = forms.ImageField(required=False)
    
class UserEditForm(UserChangeForm): #Creamos la clase UserEditForm que hereda de UserChangeForm para poder personalizar los campos que queremos mostrar en el form de UserUpdate
    
    #Hacer que no muestre el campo de contraseña
    password = forms.CharField(
        help_text="",
        widget = forms.HiddenInput(), 
        required = False
    )
    
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput) #Widget modifica el comportamiento de cualquier campo, en este caso hacemos password imput para que no muestre la pw
    password2 = forms.CharField(label="Repita contraseña", widget=forms.PasswordInput)
        
    class Meta:
        model= User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        
    def clean_password2(self): #Usando el self es sobre el propio formulario
        print(self.cleaned_data)
        
        password2 = self.cleaned_data["password2"] #Recupera lo que se puso en password2 del formulario y se le asigna a password2 dentro de esta funcion
        
        if password2 != self.cleaned_data["password1"]: #Si es distinta a la password1 que ingresaron en el formulario
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    
class AvatarFormulario(forms.ModelForm):
    #Se hace el meta para que el formulario este vinculado al modelo Avatar
    class Meta:
        model = Avatar
        fields = ('image', ) #Se pone con , para que lo tome como una tupla, sino lo toma como una imagen
        
class CompraProductoForm(forms.Form):
    cantidad = forms.IntegerField(
        label='Cantidad a comprar',
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
