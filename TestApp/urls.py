from django.urls import path

from . import views

app_name = 'TestApp'
urlpatterns = [
    path('', views.home, name="Home"),
    path('contacto/', views.contacto, name="Contacto"),
    path('ediciones/', views.ediciones, name="Ediciones"),
    path('ponencias/', views.ponencias, name="Ponencias"),
    path('ponencias/insert/', views.insert, name="Insert"),
    path('poster/', views.poster, name="Poster"),
    path('programa/', views.programa, name="Programa"),
    path('ubicacion/', views.ubicacion, name="Ubicacion"),
    path('login/', views.login, name="Login"),
    path('informe/', views.informe, name="Informe final"),
    path('edicionesAdmin/', views.iterAdmin, name="Edicion Iteraciones"),
    path('edicionesAdmin/eliminar', views.remove_iteration, name="Borrando Iteracion"),
    path('inicioAdmin/', views.inicioAdmin, name="Edición Inicio"),
    path('contactoAdmin/', views.contactoAdmin, name="Edición Contacto"),
    path('constancias/', views.constancias, name="Constancias"),
    path('report/', views.report),
    path('correos/', views.correos, name="Correos"),
    path('sendmail/', views.send_email),
]

