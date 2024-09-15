
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import CustomUser,Repartidor
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.views.generic import UpdateView,ListView,CreateView,UpdateView
from .forms import RepartidorForm
from django.urls import reverse_lazy
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
CustomUser = get_user_model()
from .models import Cliente
from django.http import JsonResponse,HttpResponseBadRequest

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def group_required(group_name):
    def decorator(view_func):
        @login_required(login_url='seguridad_app:inicio_sesion')
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('seguridad_app:noAccess')
        return _wrapped_view
    return decorator


#Vista de crud de usuarios
@group_required('Jefe')
def crudUsuarios(request):
    user_list = CustomUser.objects.filter(is_superuser=False, is_active=True).order_by('date_joined')
    return render(request, 'moduloUsuarios/crud.html', {'user_list': user_list})

#Vista de formulario para agregar usuario
@group_required('Jefe')
def agregarUsuario(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        username = request.POST['username']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        password = request.POST['password1']
        email = request.POST['email']
        dui = request.POST.get('dui')  # Puede ser None si no se proporciona
        telefono = request.POST.get('telefono')
        password2= request.POST['password2']

        #validaciones adicionales
        #No campos vacios
        if not username or not nombres or not apellidos or not password or not email or not dui or not telefono or not password2:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/crear.html')
        
        #verificar nombre de usuario existente
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya existe, por favor ingrese uno distinto')
            return render(request, 'moduloUsuarios/crear.html')
        
        #verificar que el dui es unico
        if CustomUser.objects.filter(dui=dui).exists():
            messages.error(request, 'Error al ingresar documento de identidad, el numero ingresado ya esta registrado')
            return render(request, 'moduloUsuarios/crear.html')
        
        #verificar emial
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'La direccion de correo electronica ya esta en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/crear.html')
        
        #validacion del formato del email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,'El formato del correo electrónico no es valido')
            return render(request, 'moduloUsuarios/crear.html')    
        
        #validacion de parametros
        if len(nombres) > 10:
            messages.error(request, 'Nombres demasiado extensos, trate de usar abreviaciones como: David G. Aguilar')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(apellidos) > 10:
            messages.error(request, 'Apellidos demasiado extensos, trate de usar abreviaciones como: G. Aguilar')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(dui) != 10:
            messages.error(request, 'Numero de documento de identidad no valido')
            return render(request, 'moduloUsuarios/crear.html')
        
        if len(telefono) != 9:
            messages.error(request, 'Numero de telefono no valido')
            return render(request, 'moduloUsuarios/crear.html')
        
        #longitud de contraseña
        if len(password) <8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'moduloUsuarios/crear.html')

        #validacion de contraseñas
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'moduloUsuarios/crear.html')
        
        try:
            #creacion de usuario
            user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            dui=dui,
            telefono=telefono,
            nombres=nombres,
            apellidos=apellidos
            )
            return redirect('/usuarios/')  # o cualquier otra página después del registro
        except Exception as e:
            messages.error(request, f'Error al crear el usuario: {str(e)}')
            return render(request, 'moduloUsuarios/crear.html')
    else:
        return render(request, 'moduloUsuarios/crear.html')
        #return render(request, 'moduloUsuarios/crud.html')
    

    #return render(request, 'moduloUsuarios/crear.html')

#template agregar
@group_required('Jefe')
def newuser(request):
    return render(request, 'moduloUsuarios/crear.html')

#vista de modificar usuario
@group_required('Jefe')
def modUsuario(request):
    if request.method == 'POST':
        pk=request.POST['id']
        user = get_object_or_404(CustomUser, idUsuario=pk)
        user.nombres = request.POST['nombres']
        user.apellidos = request.POST['apellidos']
        user.dui = request.POST['dui']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.telefono = request.POST.get('telefono')

        #validaciones
        #No campos vacios
        if not user.username or not user.nombres or not user.apellidos or not user.email or not user.dui or not user.telefono:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #verificar nombre de usuario existente
        if CustomUser.objects.filter(username=user.username).exclude(idUsuario=pk).exists():
            messages.error(request, 'Este nombre de usuario ya existe, por favor ingrese uno distinto')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #verificar emial
        if CustomUser.objects.filter(email=user.email).exclude(idUsuario=pk).exists():
            messages.error(request, 'La direccion de correo electronica ya esta en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        #validacion del formato del email
        try:
            validate_email(user.email)
        except ValidationError:
            messages.error(request,'El formato del correo electrónico no es valido')
            return render(request, 'moduloUsuarios/modificar.html',{'user':user})
        
        #validacion de parametros
        if len(user.nombres) > 50:
            messages.error(request, 'Nombres demasiado extensos, trate de usar abreviaciones como: David G. Aguilar')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.apellidos) > 50:
            messages.error(request, 'Apellidos demasiado extensos, trate de usar abreviaciones como: G. Aguilar')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.dui) != 10:
            messages.error(request, 'Numero de documento de identidad no valido')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        if len(user.telefono) != 9:
            messages.error(request, 'Numero de telefono no valido')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
        try:
            user.save()
            return redirect("/usuarios/")
        except Exception as e:
            messages.error(request, f'Error al modificar el usuario: {str(e)}')
            return render(request, 'moduloUsuarios/modificar.html', {'user': user})
        
    return redirect("/usuarios/")

#vista para ver usuario
@group_required('Jefe')
def verUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/modificar.html',{'user':user})

#vista inspeccionar usuario
@group_required('Jefe')
def inspeccionarUsuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    return render(request, 'moduloUsuarios/inspeccionarUsuario.html',{'user':user})

#eliminar
@group_required('Jefe')
def eliminar_usuario(request, pk):
    user = get_object_or_404(CustomUser, idUsuario=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('/usuarios/')
    return render(request,'moduloUsuarios/eliminarUsuario.html',{'user':user})
    
    


#Vistas para el submodulo de usuarios Gestion de Clientes 
#vista de crud Clientes

@group_required('Jefe')
def crudCliente(request):
    client_list = Cliente.objects.filter(estado=True)
    return render(request, 'moduloUsuarios/crudCliente.html', {'client_list': client_list})

#vista agregarCliente
@group_required('Jefe') 
def agregarClientes(request):
    if request.method == 'POST':
        # Recuperar los datos del formulario
        nombreCliente = request.POST['nombres']
        apellidoCliente = request.POST['apellidos']
        duiCliente = request.POST['dui']
        nacionalidadCliente = request.POST['nacionalidad']
        telefonoCliente = request.POST['telefono']
        emailCliente = request.POST['email']

        # Validaciones adicionales
        # No campos vacíos
        if not nombreCliente or not apellidoCliente or not duiCliente or not nacionalidadCliente or not telefonoCliente or not emailCliente:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Verificar que el DUI es único
        if Cliente.objects.filter(duiCliente=duiCliente).exists():
            messages.error(request, 'Error al ingresar documento de identidad, el número ingresado ya está registrado')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Verificar email
        if Cliente.objects.filter(emailCliente=emailCliente).exists():
            messages.error(request, 'La dirección de correo electrónico ya está en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Validación del formato del email
        try:
            validate_email(emailCliente)
        except ValidationError:
            messages.error(request, 'El formato del correo electrónico no es válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        # Validación de parámetros
        if len(nombreCliente) > 50:
            messages.error(request, 'Nombre demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(apellidoCliente) > 50:
            messages.error(request, 'Apellido demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(duiCliente) != 10:
            messages.error(request, 'Número de documento de identidad no válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        if len(telefonoCliente) != 9:
            messages.error(request, 'Número de teléfono no válido')
            return render(request, 'moduloUsuarios/crearCliente.html')

        try:
            # Creación de cliente
            cliente = Cliente.objects.create(
                nombreCliente=nombreCliente,
                apellidoCliente=apellidoCliente,
                duiCliente=duiCliente,
                nacionalidadCliente=nacionalidadCliente,
                telefonoCliente=telefonoCliente,
                emailCliente=emailCliente
            )
            return redirect('/usuarios/crudCliente')  # o cualquier otra página después del registro
        except Exception as e:
            messages.error(request, f'Error al crear el cliente: {str(e)}')
            return render(request, 'moduloUsuarios/crearCliente.html')
    else:
        return render(request, 'moduloUsuarios/crearCliente.html')

#renderizar html crearCliente
@group_required('Jefe')
def newCliente(request):
    return render(request, 'moduloUsuarios/crearCliente.html')

#Vista de formulario para modificar cliente
@group_required('Jefe')
def modificarClientes(request):
    if request.method == 'POST':
        pk = request.POST['idCliente']
        cliente = get_object_or_404(Cliente, idCliente=pk)
        cliente.nombreCliente = request.POST['nombres']
        cliente.apellidoCliente = request.POST['apellidos']
        cliente.duiCliente = request.POST['dui']
        cliente.nacionalidadCliente = request.POST['nacionalidad']
        cliente.telefonoCliente = request.POST.get('telefono')
        cliente.emailCliente = request.POST['email']

        # Validaciones
        # No campos vacíos
        if not cliente.nombreCliente or not cliente.apellidoCliente or not cliente.emailCliente or not cliente.duiCliente or not cliente.telefonoCliente or not cliente.nacionalidadCliente:
            messages.error(request, 'Por favor complete todos los campos obligatorios')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Verificar que el DUI es único
        if Cliente.objects.filter(duiCliente=cliente.duiCliente).exclude(idCliente=pk).exists():
            messages.error(request, 'Error al ingresar documento de identidad, el número ingresado ya está registrado')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Verificar email
        if Cliente.objects.filter(emailCliente=cliente.emailCliente).exclude(idCliente=pk).exists():
            messages.error(request, 'La dirección de correo electrónico ya está en uso, por favor ingrese otro email')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Validación del formato del email
        try:
            validate_email(cliente.emailCliente)
        except ValidationError:
            messages.error(request, 'El formato del correo electrónico no es válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        # Validación de parámetros
        if len(cliente.nombreCliente) > 50:
            messages.error(request, 'Nombre demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.apellidoCliente) > 50:
            messages.error(request, 'Apellido demasiado extenso, trate de usar abreviaciones')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.duiCliente) != 10:
            messages.error(request, 'Número de documento de identidad no válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        if len(cliente.telefonoCliente) != 9:
            messages.error(request, 'Número de teléfono no válido')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})
        
        try:
            cliente.save()
            return redirect("/usuarios/crudCliente/")
        except Exception as e:
            messages.error(request, f'Error al modificar el cliente: {str(e)}')
            return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})

    return redirect("/usuarios/crudCliente/")

#verificar cliente
@group_required('Jefe')
def verificarCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    return render(request, 'moduloUsuarios/inspeccionarCliente.html', {'cliente': cliente})

#eliminar
@group_required('Jefe')
def deleteCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    if request.method == 'POST':
        cliente.estado = False
        cliente.save()
        return redirect('/usuarios/crudCliente/')
    return render(request, 'moduloUsuarios/eliminarCliente.html',{'cliente':cliente})

#vista para ver usuario
@group_required('Jefe')
def verCliente(request, pk):
    cliente = get_object_or_404(Cliente, idCliente=pk)
    return render(request, 'moduloUsuarios/modificarCliente.html', {'cliente': cliente})



	#--------------------------- Modulo Repartidor----------------------

#vista crear
class crear_repartidor(CreateView):
    form_class = RepartidorForm
    success_url = reverse_lazy('moduloUsuarios:crud_repartidor')
    template_name = 'moduloUsuarios/crearRepartidor.html'



#vista listar repartidores
@method_decorator(group_required('Jefe'), name='dispatch')
class crud_repartidor(ListView):
    template_name = "moduloUsuarios/crudRepartidor.html"
    model = Repartidor
    context_object_name = "lista_Repartidor"
    # paginate_by=7
    # queryset=Repartidor.objects.all()

#vista ver datos repartidor
@group_required('Jefe')
def ver_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)
    return render(
        request, "moduloUsuarios/verRepartidor.html", {"repartidor": repartidor}
    )

#vista modificar repartidor
@method_decorator(group_required('Jefe'), name='dispatch')
class modificar_repartidor(UpdateView):
    template_name = "moduloUsuarios/modificarRepartidor.html"
    model = Repartidor
    form_class = RepartidorForm
    success_url = reverse_lazy("moduloUsuarios:crud_repartidor")

    def form_valid(self, form):
        messages.success(self.request, "El Repartidor se ha modificado exitosamente")
        return super().form_valid(form)
    
#vista eliminar repartidor
@group_required('Jefe')
def eliminar_repartidor(request, pk):
    repartidor = get_object_or_404(Repartidor, pk=pk)

    if request.method == "POST":
        try:
            repartidor.delete()
            # Agregar mensaje de éxito
            messages.success(request, 'Repartidor eliminado correctamente!')
        except Exception as e:
            # Agregar mensaje de error si ocurre una excepción
            messages.error(request, f'Error al eliminar el repartidor: {str(e)}')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Repartidor eliminado correctamente!'})
        return redirect("moduloUsuarios:crud_repartidor")

    return render(request, "moduloUsuarios/eliminarRepartidor.html", {"repartidor": repartidor})
	