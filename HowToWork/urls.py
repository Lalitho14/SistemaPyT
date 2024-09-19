from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.registro, name='register'),
    path('proyectos/', views.VerProyectos, name='proyectos'),
    path('logout/', views.Salir, name='salir'),
    path('login/', views.IniciarSesion, name='login'),
    path('amigos/', views.VerAmigos, name='amigos'),
    path('buscar/', views.BuscarAmigos, name='buscar'),
    path('vista_proyecto/<int:id_proyecto>', views.VistaProyecto, name='vista_proyecto'),
    path('vista_proyecto/<int:id_proyecto>/delete', views.Delete_Proyecto, name='delete_proyecto')
]
