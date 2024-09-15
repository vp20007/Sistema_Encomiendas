from django import forms
from .models import Viaje

class CrearViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['fecha_ida', 'fecha_vuelta', 'destino', 'cantidad_personas', 'precio_boleto_ida', 'precio_boleto_retorno']
       # fields='__all__'
        widgets={'fecha_ida': forms.DateInput(attrs={'type':'date'})}
        widgets={'fecha_vuelta': forms.DateInput(attrs={'type':'date'})}

