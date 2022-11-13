from django.urls import path, include

from . import views

app_name = 'TestApp'
urlpatterns = [
    path('', views.home, name="Home"),
    path('contacto/', views.contacto, name="Contacto"),
    path('ediciones/', views.ediciones, name="Ediciones"),
    path('ponencias/', views.ponencias, name="Ponencias"),

    path('poster/', views.poster, name="Poster"),
    path('programa/', views.programa, name="Programa"),
    path('ubicacion/', views.ubicacion, name="Ubicacion"),


    # URLs de la interfaz del admin
    path('admin/home/', views.baseFront, name="BaseFront"),


    path('informe/', views.informe, name="Informe final"),
    path('admin/edicionesAdmin/', views.iterAdmin, name="Edicion Iteraciones"),
    path('admin/edicionesAdmin/eliminar', views.remove_iteration, name="Borrando Iteracion"),
    path('inicioAdmin/', views.inicioAdmin, name="Edición Inicio"),
    path('contactoAdmin/', views.contactoAdmin, name="Edición Contacto"),
    path('constancias/', views.constancias, name="Constancias"),
    path('report/', views.report),


    path('admin/', include('django.contrib.auth.urls')),
    path('admin/', views.administrador_redirect_login),

    path('correos/', views.correos, name="Correos"),
    path('sendmail/', views.send_email),
    path('add/', views.AddPresentation),
    #path('addauthor/', views.AddPresentation),

]

