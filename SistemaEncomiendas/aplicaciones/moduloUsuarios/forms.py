from django.forms import ModelForm
from django import forms
from .models import Repartidor,Cliente

import re
from django.core.exceptions import ValidationError
from .validators import validar_dui,validar_telefono



class RepartidorForm(forms.ModelForm):
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    DUI_persona = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DUI','id':'DUI','maxlength':'10'}),validators=[validar_dui])
    telefono_repartidor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono','id':'tel','maxlength':'9'}),validators=[validar_telefono])
    class Meta:
        model = Repartidor
        fields = [ 'nombres', 'apellidos', 'DUI_persona', 'telefono_repartidor']

class ClienteForm(forms.ModelForm):
    duiCliente=forms.CharField(validators=[validar_dui])
    class meta:
        model= Cliente
        fields = [ 'nombreCliente', 'apellidoCliente', 'duiCliente', 'nacionalidadCliente','telefonoCliente','emailCliente']
        
