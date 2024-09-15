from django.urls import path
from . import views

app_name = 'moduloViajes'

urlpatterns = [
    path('editar/<int:pk>/',views.editar_viaje, name="editarviaje"),
    path('',views.mostrar_viajes, name="listaviajes"),
    path('filtro/',views.mostrar_viajes_filtrados, name="filtroviajes"),
    path('nuevo/',views.crear_viaje, name="nuevo"),
    path('eliminar/<int:pk>/', views.eliminar_viaje, name='eliminarviaje'),
    path('<int:pk>/', views.ver_viaje, name='verviaje'),
]