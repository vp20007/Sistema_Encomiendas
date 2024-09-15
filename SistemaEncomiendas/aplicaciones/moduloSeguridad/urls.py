from django.urls import path
from . import views

app_name = 'seguridad_app'
urlpatterns = [
    path('login/', views.LoginUser.as_view(),name='inicio_sesion'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('noaccess/', views.no_access_view,name='noAccess'),
    path('cambio-contraseña/', views.ChangePasswordView.as_view(),name='cambioContaseña'),
    path('home/',views.home,name='home'),
    path('crud/', views.crud,name='CRUD'),
    path('registro/', views.registro,name='registro'),
    path('create-superuser/', views.create_superuser, name='create_superuser'),
]
