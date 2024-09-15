from django.db import models
from ..moduloUsuarios.models import Cliente
from ..moduloViajes. models import Viaje
from ..moduloSeguimiento.models import Ruta,Recordatorio
from ..moduloArticulos.models import Articulo

# Create your models here.
class Paquete(models.Model):
    id_paquete = models.AutoField(primary_key=True)
    id_articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT)
    destinatario = models.CharField(max_length=50)
    total_peso_pa = models.DecimalField(max_digits=10, decimal_places=2)
    
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_viaje = models.ForeignKey(Viaje, on_delete=models.RESTRICT)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    id_ruta = models.ForeignKey(Ruta, on_delete=models.RESTRICT)
    id_paquete = models.ForeignKey(Paquete, on_delete=models.RESTRICT)
    id_ubicacion = models.ForeignKey(Recordatorio, on_delete=models.RESTRICT)
    numero_de_orden = models.CharField(max_length=20)
    fecha_pedido = models.DateField()
    punto_entrega = models.CharField(max_length=100)
    punto_recepcion = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    estado_pedido = models.CharField(max_length=12)
    recogido = models.BooleanField()
    total_peso_pe = models.DecimalField(max_digits=10, decimal_places=2)
    img_pedido = models.CharField(max_length=255)