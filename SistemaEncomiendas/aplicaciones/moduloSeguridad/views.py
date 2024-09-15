from django.shortcuts import render
from django.shortcuts import redirect
from .forms import LoginForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from aplicaciones.moduloUsuarios.models import CustomUser
from django.http import HttpResponse
# Create your views here.
def no_access_view(request):
    return render(request, 'moduloSeguridad/accesoDen.html')

def crud(request):
    return render(request,'moduloSeguridad/crud.html')

def registro(request):
    return render(request,'moduloSeguridad/registro.html')

class LoginUser(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('seguridad_app:home')
    template_name = 'moduloSeguridad/login.html'
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        credenciales = form.cleaned_data
        user = authenticate(username=credenciales['username'],password=credenciales['password'])
        
        
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, 'Bienvenido, {}'.format(username))
            next_url = self.request.GET.get('next', self.success_url)
            return redirect(next_url)
        else:
                messages.add_message(self.request, messages.ERROR,'Error: credenciales incorrectas ')
                return redirect(reverse_lazy('seguridad_app:inicio_sesion'))
            
        

def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Sesión cerrada, hasta luego.")
    return render(request,'home2.html')

class ChangePasswordView(FormView):
    template_name = 'moduloseguridad/cambiarContraseña.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('seguridad_app:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  
        messages.success(self.request, 'Tu contraseña ha sido actualizada correctamente.')
        return super().form_valid(form)

def home(request):
    return render(request,'home2.html')


def create_superuser(request):
    username = 'admin1'
    email = 'admin1@example.com'
    password = '*12345Aad*'
    
    if CustomUser.objects.filter(username=username).exists():
        return HttpResponse('El nombre de usuario ya existe.')
    
    CustomUser.objects.create_superuser(username, email, password)
    return HttpResponse(f'Superusuario {username} creado con éxito.')
