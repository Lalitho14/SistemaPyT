from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Tarea


class Registro(UserCreationForm):
  username = forms.CharField(
      label='Nombre de Usuario', min_length=5, max_length=45)
  email = forms.EmailField(label='Correo')
  password1 = forms.CharField(label='Contrasenia', widget=forms.PasswordInput)
  password2 = forms.CharField(
      label='Confirmar Contrasenia', widget=forms.PasswordInput)
  usable_password = None

  def username_clean(self):
    username = self.cleaned_data['username'].lower()
    new = User.objects.filter(username=username)
    if new.count():
      raise ValidationError('Usuario ya registrado')
    return username

  def email_clean(self):
    email = self.cleaned_data['email'].lower()
    new = User.objects.filter(email=email)
    if new.count():
      raise ValidationError('Correo ya registrado')
    return email

  def clean_password2(self):
    password1 = self.cleaned_data['password1']
    password2 = self.cleaned_data['password2']

    if password1 and password2 and password1 != password2:
      raise ValidationError('Contrasenias no coinciden')
    return password2

  def save(self, commit=True):
    user = User.objects.create_user(
        self.cleaned_data['username'],
        self.cleaned_data['email'],
        self.cleaned_data['password1']
    )
    return user


class BuscarUsuario(forms.Form):
  username = forms.CharField(label="",max_length=45)


class EnviarSolicitudAmistad(forms.Form):
  id_usr2 = forms.IntegerField(widget=forms.HiddenInput)


class AceptarSolicitudAmistad(forms.Form):
  id_usr1 = forms.IntegerField(widget=forms.HiddenInput)


class CrearNuevoProyecto(forms.Form):
  nombre = forms.CharField(label="Nombre del Proyecto", max_length=45)
  descripcion = forms.CharField(
    label="Descripcion del proyecto", max_length=255, widget=forms.Textarea)
  id_usr = forms.IntegerField(widget=forms.HiddenInput)


class SolicitudProyecto(forms.Form):
  id_usr = forms.IntegerField(widget=forms.HiddenInput)


class AceptarSolicitudProyecto(forms.Form):
  aceptar = 'Aceptar'
  rechazar = 'Rechazar'

  decision = [
    (aceptar, 'Aceptar'),
    (rechazar, 'Rechazar')
  ]

  opcion = forms.ChoiceField(
    choices=decision, widget=forms.HiddenInput, required=False)
  id_proyecto = forms.IntegerField(widget=forms.HiddenInput)


class CrearTarea(forms.Form):
  id_proyecto = forms.IntegerField(widget=forms.HiddenInput)
  nombre = forms.CharField(label="Nombre de la Tarea", max_length=45)
  descripcion = forms.CharField(
    label="Descripcion", max_length=255, widget=forms.Textarea)

class StatusTarea(forms.Form):
  opciones = (
    (0, 'Pendiente'),
    (1, 'Completada'),
    (2, 'Necesita Revision')
  )
  
  new_status = forms.ChoiceField(choices=opciones, label="Status")
  id_tarea = forms.CharField(widget=forms.HiddenInput)
