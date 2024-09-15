from django.db import models

class Articulo(models.Model):
    id_articulo = models.AutoField(primary_key=True)
    id_servicio = models.ForeignKey('Servicio', on_delete=models.RESTRICT)
    id_ti_articulo = models.ForeignKey('TipoArticulo', on_delete=models.RESTRICT)
    id_lis_marcas = models.ForeignKey('ListadoMarcas', on_delete=models.RESTRICT)
    id_lis_impuesto = models.ForeignKey('ListadoImpuesto', on_delete=models.RESTRICT)
    id_cancelacion = models.ForeignKey('Cancelacion', on_delete=models.RESTRICT, null=True, blank=True)
    nombre_articulo = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    canrtidad = models.IntegerField()
    estado = models.CharField(max_length=30)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)

class TipoArticulo(models.Model):
    id_ti_articulo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50)
    precio_libra = models.DecimalField(max_digits=10, decimal_places=2)

class Cancelacion(models.Model):
    id_cancelacion = models.AutoField(primary_key=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    precio_envio = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=200)
    tipo_cancelacion = models.CharField(max_length=30)

class ListadoImpuesto(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Par', 'Par'),
        ('Unidad', 'Unidad'),
        ('Set', 'Set'),
        ('Conjunto', 'Conjunto'),
        ('Kilogramo', 'Kilogramo'),
        ('Docena', 'Docena'),
        ('Paquete', 'Paquete'),
        ('Juego', 'Juego'),
        ('Caja', 'Caja'),
        ('Bote', 'Bote'),
        ('Bolsa/Caja', 'Bolsa/Caja'),
        ('Botella', 'Botella'),
        ('Bolsa', 'Bolsa'),
        ('Libra', 'Libra'),
        ('Lata', 'Lata'),
        ('Caja', 'Caja'),
        ('Frasco', 'Frasco'),
        ('Equipo', 'Equipo'),
        ('Metro', 'Metro'),
        ('Yarda', 'Yarda'),
        ('Ramo', 'Ramo'),
        ('Kit', 'Kit'),
        ('Gramo', 'Gramo'),
        ('Pliego', 'Pliego'),
    ]
    id_lis_impuesto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=10,choices=UNIDAD_MEDIDA_CHOICES)
    cip = models.DecimalField(max_digits=10, decimal_places=2)
    fob = models.DecimalField(max_digits=10, decimal_places=2)

class ListadoMarcas(models.Model):
    id_lis_marcas = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=50)
