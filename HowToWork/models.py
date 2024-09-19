from django.db import models
# from django.contrib.auth.hashers import make_password, check_password
# Create your models here.
# Modelo para Usario
from django.contrib.auth.models import User as Usuario
# Modelo para solicitudes de amistad entre usuario


class SolicitudAmistad(models.Model):
  id_usr1 = models.ForeignKey(
    Usuario, on_delete=models.CASCADE, related_name='fk_usr1')
  id_usr2 = models.ForeignKey(
    Usuario, on_delete=models.CASCADE, related_name='fk_usr2')
  status = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.id_usr1.username + ' - ' + self.id_usr2.username

# Modelo para proyecto


class Proyecto(models.Model):
  nombre = models.CharField(max_length=45, null=False)
  descripcion = models.CharField(max_length=255, null=False)
  usuarios = models.ManyToManyField(
    Usuario,
    blank=True,
    related_name='proyectousuario'
  )

  def __str__(self) -> str:
    return self.nombre
# Modelo para tarea


class Tarea(models.Model):
  nombre = models.CharField(max_length=45, null=False)
  descripcion = models.CharField(max_length=255, null=False)
  notas = models.CharField(max_length=255, null=True)
  id_proyecto = models.ForeignKey(
    Proyecto, on_delete=models.CASCADE, unique=False)

  class Status(models.IntegerChoices):
    pendiente = 0, 'Pendiente'
    completado = 1, 'Completado'
    revision = 2, 'Necesita Revision'

  status = models.IntegerField(
    choices=Status.choices,
    default=Status.pendiente
  )

  def __str__(self) -> str:
    return self.nombre

# Modelo para solicitudes de entrar al proyecto entre usuarios


class SolicitudProyecto(models.Model):
  id_usr1 = models.ForeignKey(
    Usuario, on_delete=models.CASCADE, related_name='fk_usr1proyecto')
  id_usr2 = models.ForeignKey(
    Usuario, on_delete=models.CASCADE, related_name='fk_usr2proyecto')
  id_proyecto = models.ForeignKey(
    Proyecto, on_delete=models.CASCADE, related_name='fk_proyecto', null=True)
  status = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.status
