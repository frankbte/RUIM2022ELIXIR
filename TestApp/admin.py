from django.contrib import admin
from TestApp.models import PresentacionRegistro, InicioPage, ProgramaPage, PosterPage, RegistroPage, UbicacionPage, \
    ContactoPage, EdicionesPage, Evento, Author

# Register your models here.

class AuthorInfo(admin.ModelAdmin):
    list_display = ("nombre_completo",  "institucion", "departamento", "grado")
    list_filter = ("grado","institucion", "departamento")

    @admin.display()
    def nombre_completo(self, obj):
        return obj.nombre + ' ' + obj.apellido_pat + ' ' + obj.apellido_mat

class PresentationRegistroInfo(admin.ModelAdmin):
    list_display = ("presentacion_titulo", "responsable", "modalidad", "Evento", "estatus")
    list_filter = ("modalidad","estatus")

    @admin.display()
    def responsable(self, obj):
        return obj.resp.nombre + ' ' + obj.resp.apellido_pat + ' ' + obj.resp.apellido_mat

    @admin.display()
    def Evento(self, obj):
        return "RUIM " + str(obj.evento.year)

class EventoInfo(admin.ModelAdmin):
    list_display = ("Edición", "lugar", "fecha", "active")

    @admin.display()
    def Edición(self, obj):
        return "RUIM " + str(obj.year)

admin.site.register(PresentacionRegistro,PresentationRegistroInfo)
admin.site.register(InicioPage)
admin.site.register(ProgramaPage)
admin.site.register(PosterPage)
admin.site.register(RegistroPage)
admin.site.register(UbicacionPage)
admin.site.register(ContactoPage)
admin.site.register(EdicionesPage)
admin.site.register(Author,AuthorInfo)
admin.site.register(Evento, EventoInfo)