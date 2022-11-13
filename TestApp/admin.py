from django.contrib import admin
from TestApp.models import PresentacionRegistro, InicioPage, ProgramaPage, PosterPage, RegistroPage, UbicacionPage, \
    ContactoPage, EdicionesPage, Evento, Author

# Register your models here.

class AuthorInfo(admin.ModelAdmin):
    list_display = ("nombre", "apellido_pat", "apellido_mat", "institucion")

class PresentationRegistroInfo(admin.ModelAdmin):
    list_display = ("presentacion_titulo", "resp", "modalidad", "estatus", "evento")

admin.site.register(PresentacionRegistro,PresentationRegistroInfo)
admin.site.register(InicioPage)
admin.site.register(ProgramaPage)
admin.site.register(PosterPage)
admin.site.register(RegistroPage)
admin.site.register(UbicacionPage)
admin.site.register(ContactoPage)
admin.site.register(EdicionesPage)
admin.site.register(Author,AuthorInfo)
admin.site.register(Evento)