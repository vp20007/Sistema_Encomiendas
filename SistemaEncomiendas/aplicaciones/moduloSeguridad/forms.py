from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg ', 'autocomplete': 'on'}),
        error_messages={
            'required': 'Por favor ingrese su nombre de usuario.',
            'max_length': 'El nombre de usuario no puede exceder los 50 caracteres.'
        }
    )
    password = forms.CharField(
        label='Contraseña',
        max_length=10,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        error_messages={
            'required': 'Por favor ingrese su contraseña.',
            'max_length': 'La contraseña no puede exceder los 100 caracteres.'
        }
    )
    
    
    

class ChangePasswordForm(PasswordChangeForm):
    error_messages = {
        'password_incorrect': ("Tu contraseña antigua es incorrecta. Por favor, intenta de nuevo."),
        'password_mismatch': ("Las contraseñas no coinciden."),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña Actual'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva Contraseña'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar Nueva Contraseña'
        })
        
    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        user = self.user

        if not user.check_password(old_password):
            raise forms.ValidationError("La contraseña antigua es incorrecta!!!.")

        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Las contraseñas nuevas no coinciden!!!.")

        return cleaned_data