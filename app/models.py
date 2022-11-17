from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)


class Equipo(models.Model):
    serial_equipo = models.CharField(max_length=255, null=False, primary_key=True)
    modelo = models.CharField(max_length=100, null=False)
    marca = models.CharField(max_length=255, null=False)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    area = models.CharField(max_length=100, null=False, blank=True)
    piso = models.CharField(max_length=100, null=False, blank=True)
    estado = models.BooleanField(default=False)
    estatus = models.BooleanField(default=False)
    ingreso = models.DateTimeField(auto_now_add=True)
    retiro = models.DateTimeField(null=True, blank=True)


class Configuracion(models.Model):
    nombre = models.CharField(max_length=100),
    serial_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    ruta_script = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=255, null=True)
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=False, blank=True)
    creado = models.DateTimeField(auto_now_add=True)


class ClienteGeneraConf(models.Model):
    configuracion = models.ForeignKey(Configuracion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TipoNovedad(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)


class Novedad(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    tipo_novedad = models.ForeignKey(TipoNovedad, on_delete=models.CASCADE)
    motivo = models.TextField()
    serial_equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)


class ClienteGeneraNovedad(models.Model):
    novedad = models.ForeignKey(Novedad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AdmonGeneraNovedad(models.Model):
    novedad = models.ForeignKey(Novedad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ClienteRegistraEquipo(models.Model):
    Equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ClienteGeneraScript(models.Model):
    archivo = models.FileField(upload_to="Uploaded media/")
    Equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
