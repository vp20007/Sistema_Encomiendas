
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractUser):
    idUsuario=models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=50, blank=True, null=False)
    apellidos = models.CharField(max_length=50, blank=True, null=False)
    dui = models.CharField(max_length=10, blank=True, null=True, unique=True)
    activo = models.BooleanField(default=True)
    telefono =  models.CharField(max_length=10, blank=True, null=False)

class Cliente(models.Model):
    idCliente=models.BigAutoField(primary_key=True)
    nombreCliente=models.CharField(max_length=50,blank=True, null=False)
    apellidoCliente=models.CharField(max_length=50,blank=True, null=False)
    duiCliente=models.CharField(max_length=10,blank=True, null=False)
    nacionalidadCliente=models.CharField(max_length=50,blank=True, null=False)
    telefonoCliente=models.CharField(max_length=10,blank=True, null=False)
    emailCliente=models.CharField(max_length=50,blank=True, null=False)
    estado = models.BooleanField('estado', default=True)
    
class Repartidor(models.Model):
    id_repartidor = models.AutoField(primary_key=True)
    nombres=models.CharField(max_length=50)
    apellidos=models.CharField(max_length=50)
    DUI_persona=models.CharField(max_length=10,unique=True)
    telefono_repartidor=models.CharField(max_length=10, blank=True, null=False)
    

class Telefono(models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    codigo_pais = models.CharField(max_length=3)
    numero = models.CharField(max_length=10)
