from django.shortcuts import render, redirect, get_object_or_404
from .forms import Registro, BuscarUsuario, EnviarSolicitudAmistad, AceptarSolicitudAmistad, CrearNuevoProyecto, AceptarSolicitudProyecto, CrearTarea, StatusTarea
from .models import Usuario, SolicitudAmistad, Proyecto, SolicitudProyecto, Tarea
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here


def index(requests):
  return render(requests, "index.html")


def registro(requests):
  if requests.method == 'GET':
    return render(requests, "accounts/signup.html", {
        'form': Registro
    })
  else:
    if requests.POST['password1'] == requests.POST['password2']:
      try:
        user = Usuario.objects.create_user(
            username=requests.POST['username'], password=requests.POST['password1'], email=requests.POST['email']
        )
        user.save()
        login(requests, user)
        return redirect('proyectos')
      except IntegrityError:
        return render(requests, 'accounts/signup.html', {
            'form': Registro,
            'error': 'Usuario registrado'
        })
    return render(requests, 'accounts/signup.html', {
        'form': Registro,
        'error': 'Las contrasenias no coinciden'
    })


@login_required()
def VerProyectos(requests):
  proyectos_usr = requests.user.proyectousuario.all()
  solicitud_proyectos = SolicitudProyecto.objects.filter(id_usr2=requests.user, status=False)
  if requests.method == 'GET':
    return render(requests, 'proyectos.html', {
        'proyectos_usr': proyectos_usr,
        'solicitudes': solicitud_proyectos,
        'form': CrearNuevoProyecto(initial={'id_usr': requests.user.id}),
        'aceptar': AceptarSolicitudProyecto
    })
  else:
    if 'id_usr' in requests.POST:
      new_proyecto = Proyecto.objects.create(
          nombre=requests.POST['nombre'],
          descripcion=requests.POST['descripcion'],
      )
      new_proyecto.usuarios.set(requests.POST['id_usr'])
      return render(requests, 'proyectos.html', {
          'proyectos_usr': proyectos_usr,
          'solicitudes': solicitud_proyectos,
          'form': CrearNuevoProyecto(initial={'id_usr': requests.user.id}),
          'aceptar': AceptarSolicitudProyecto
      })
    elif 'decision' in requests.POST:
      decision = requests.POST['decision']
      id_p = Proyecto.objects.get(id=requests.POST['id_proyecto'])
      soli = SolicitudProyecto.objects.get(id_usr2=requests.user, id_proyecto=id_p)
      if decision == AceptarSolicitudProyecto.aceptar:
        id_p.usuarios.add(requests.user  )
        soli.status = True
        soli.save()
        return render(requests, 'proyectos.html', {
            'proyectos_usr': proyectos_usr,
            'solicitudes': solicitud_proyectos,
            'form': CrearNuevoProyecto(initial={'id_usr': requests.user.id}),
            'aceptar': AceptarSolicitudProyecto
        })
      elif decision == AceptarSolicitudProyecto.rechazar:
        soli.delete()
        return render(requests, 'proyectos.html', {
          'proyectos_usr': proyectos_usr,
          'solicitudes': solicitud_proyectos,
          'form': CrearNuevoProyecto(initial={'id_usr': requests.user.id}),
          'aceptar': AceptarSolicitudProyecto
        })


def Salir(requests):
  logout(requests)
  return redirect('index')


def IniciarSesion(requests):
  if requests.method == 'GET':
    return render(requests, 'accounts/login.html', {
        'form': AuthenticationForm
    })
  else:
    user = authenticate(
        requests, username=requests.POST['username'], password=requests.POST['password'])
    if user is None:
      return render(requests, 'accounts/login.html', {
          'form': AuthenticationForm,
          'error': 'Datos incorrectos'
      })
    else:
      login(requests, user)
      return redirect('proyectos')


def VerAmigos(requests):
  amigos = SolicitudAmistad.objects.filter(
    status=True, id_usr1=requests.user.id)
  lista_amigos = []

  amigos = amigos.union(SolicitudAmistad.objects.filter(
    status=True, id_usr2=requests.user.id))

  for amigo in amigos:
    if amigo.id_usr1 == requests.user:
      lista_amigos.append(amigo.id_usr2)
    else:
      lista_amigos.append(amigo.id_usr1)

  return render(requests, 'amigos.html', {
      'amigos': lista_amigos
  })


def BuscarAmigos(requests):
  solicitudes_env = SolicitudAmistad.objects.filter(
      id_usr1=requests.user.id).exclude(status=True)
  solicitudes_recv = SolicitudAmistad.objects.filter(
      id_usr2=requests.user.id).exclude(status=True)
  if requests.method == 'GET':
    return render(requests, 'Buscar_amigos.html', {
        'form': BuscarUsuario,
        'soli_form': EnviarSolicitudAmistad,
        'aceptar_form': AceptarSolicitudAmistad,
        'solicitudes_env': solicitudes_env,
        'solicitudes_recv': solicitudes_recv
    })
  else:
    if 'username' in requests.POST:
      usr_buscado = requests.POST['username']
      usr_buscado = Usuario.objects.filter(
          username=usr_buscado).exclude(id=requests.user.id)
      if usr_buscado:
        return render(requests, 'Buscar_amigos.html', {
            'form': BuscarUsuario,
            'solicitudes_env': solicitudes_env,
            'solicitudes_recv': solicitudes_recv,
            'soli_form': EnviarSolicitudAmistad,
            'aceptar_form': AceptarSolicitudAmistad,
            'resultados': usr_buscado
        })
      else:
        return render(requests, 'Buscar_amigos.html', {
            'form': BuscarUsuario,
            'soli_form': EnviarSolicitudAmistad,
            'solicitudes_env': solicitudes_env,
            'solicitudes_recv': solicitudes_recv,
            'aceptar_form': AceptarSolicitudAmistad,
            'error': 'No se encontro usuario'
        })
    elif 'id_usr2' in requests.POST:
      usr2 = Usuario.objects.get(id=requests.POST['id_usr2'])
      SolicitudAmistad.objects.create(
          id_usr1=requests.user, id_usr2=usr2, status=False)
      return redirect('buscar')
    elif 'id_usr1' in requests.POST:
      usr1 = Usuario.objects.get(id=requests.POST['id_usr1'])
      solicitud = SolicitudAmistad.objects.get(
          id_usr1=usr1, id_usr2=requests.user.id)
      solicitud.status = True
      solicitud.save()
      return redirect('buscar')


def VistaProyecto(requests, id_proyecto):
  proyecto = Proyecto.objects.get(id=id_proyecto)
  tareas = Tarea.objects.filter(id_proyecto=id_proyecto)
  amigos = SolicitudAmistad.objects.filter(
    status=True, id_usr1=requests.user.id)
  amigos = amigos.union(SolicitudAmistad.objects.filter(
    status=True, id_usr2=requests.user.id))
  lista_amigos = []
  for amigo in amigos:
    if amigo.id_usr1 == requests.user:
      colaborador = SolicitudProyecto.objects.filter(
        id_usr1=requests.user, id_usr2=amigo.id_usr2, id_proyecto=id_proyecto).exists()
      colaborador_ = SolicitudProyecto.objects.filter(
        id_usr1=amigo.id_usr2, id_usr2=requests.user, id_proyecto=id_proyecto).exists()
      if not colaborador and not colaborador_:
        lista_amigos.append(amigo.id_usr2)
    else:
      colaborador = SolicitudProyecto.objects.filter(
        id_usr1=requests.user, id_usr2=amigo.id_usr1, id_proyecto=id_proyecto).exists()
      colaborador_ = SolicitudProyecto.objects.filter(
        id_usr1=amigo.id_usr1, id_usr2=requests.user, id_proyecto=id_proyecto).exists()
      if not colaborador and not colaborador_:
        lista_amigos.append(amigo.id_usr1)

  if requests.method == 'GET':
    return render(requests, "vista_proyecto.html", {
        'proyecto': proyecto,
        'amigos': lista_amigos,
        'form': SolicitudProyecto,
        'nuevas_tareas': CrearTarea(initial={'id_proyecto':id_proyecto}),
        'tareas':tareas,
        'form_status': StatusTarea
    })
  else:
    if 'id_usr' in requests.POST:
      usr2 = Usuario.objects.get(id=requests.POST['id_usr'])
      proyecto = Proyecto.objects.get(id=id_proyecto)
      SolicitudProyecto.objects.create(
        id_usr1=requests.user, id_usr2=usr2, id_proyecto=proyecto, status=False)
      return redirect('vista_proyecto', id_proyecto)
    if 'nombre' in requests.POST:
      p = Proyecto.objects.get(id=id_proyecto)
      Tarea.objects.create(nombre=requests.POST['nombre'], descripcion=requests.POST['descripcion'], id_proyecto=p)
      return redirect('vista_proyecto', id_proyecto)
    if 'id_tarea' in requests.POST:
      print(requests.POST)
      t = Tarea.objects.get(id=requests.POST['id_tarea'])
      t.status = requests.POST['new_status']
      t.save()
      return redirect('vista_proyecto', id_proyecto)

def Delete_Proyecto(requests, id_proyecto):
  p = get_object_or_404(Proyecto, pk=id_proyecto)
  if requests.method == 'POST':
    p.delete()
    return redirect('proyectos')