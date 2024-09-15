from django.db import models
from ..moduloUsuarios.models import Repartidor
# Create your models here.
class Recordatorio(models.Model):
    id_recordatorio = models.AutoField(primary_key=True)
    fecha_entrega = models.DateField()
    num_peticiones = models.IntegerField()
class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    #id_repartidor = models.ForeignKey(Repartidor, on_delete=models.RESTRICT)
    nombre_ruta = models.CharField(max_length=50)
    zona = models.CharField(max_length=50)