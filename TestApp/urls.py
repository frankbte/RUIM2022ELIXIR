from django.urls import path, include

from . import views

app_name = 'TestApp'
urlpatterns = [
    path('', views.home, name="Home"),
    path('contacto/', views.contacto, name="Contacto"),
    path('ediciones/', views.ediciones, name="Ediciones"),
    path('ponencias/', views.ponencias, name="Ponencias"),
    path('registro/', views.inforegistro, name="Registro"),


    path('poster/', views.poster, name="Poster"),
    path('programa/', views.programa, name="Programa"),
    path('ubicacion/', views.ubicacion, name="Ubicacion"),

    path('cambiando_vista/<int:year>', views.change_viewing_event, name="Cambiar Vista"),

    # URLs de la interfaz del admin

    path('admin/informe/', views.informe, name="Informe final"),
    
    path('admin/edicionesAdmin/', views.iterAdmin, name="Edicion_Iteraciones"),
    path('admin/crearEdicion/', views.create_iter, name= "Crear una Iteración"),
    path('admin/insertEdicion/', views.insert_iter, name = "Insertando Iteración"),
    
    path('admin/edicionesAdmin/eliminar', views.remove_iteration, name="Borrando Iteracion"),
    path('admin/edicionesAdmin/activar', views.activate_event, name="Activar Iteracion"),
    path('admin/edicionesAdmin/editing', views.change_editing_event, name="Change Editing"),
    path('admin/inicioAdmin/', views.inicioAdmin, name="Edición Inicio"),
    
    path('admin/ponencias/', views.ponenciasAdmin, name="Estados Ponencias"),
    
    path('admin/contactoAdmin/', views.contactoAdmin, name="Edición Contacto"),
    
    path('admin/ubicacionAdmin/', views.ubicacionAdmin, name="Edición Ubicacion"),
    path('admin/processUbicacion/', views.processUbicacion),
    
    path('admin/posterAdmin/', views.posterAdmin, name="Edición Poster"),
    path('admin/processPoster/', views.processPoster),
    
    path('admin/programaAdmin/', views.programaAdmin, name="Edición Programa"),
    path('admin/processPrograma/', views.processPrograma),
    
    path('admin/constancias/', views.constancias, name="Constancias"),
    path('admin/report/', views.report),

    path('admin/', include('django.contrib.auth.urls')),
    path('admin/', views.administrador_redirect_login),

    path('admin/correos/', views.correos, name="Correos"),
    path('admin/sendmail/', views.send_email),
    
    path('add/', views.AddPresentation),
    #path('addauthor/', views.AddPresentation),

]

