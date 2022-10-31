from django.contrib import admin
from TestApp.models import PresentacionRegistro, InicioPage, ProgramaPage, PosterPage, RegistroPage, UbicacionPage, \
    ContactoPage, EdicionesPage, Evento, Author

# Register your models here.

admin.site.register(PresentacionRegistro)
admin.site.register(InicioPage)
admin.site.register(ProgramaPage)
admin.site.register(PosterPage)
admin.site.register(RegistroPage)
admin.site.register(UbicacionPage)
admin.site.register(ContactoPage)
admin.site.register(EdicionesPage)
admin.site.register(Author)
admin.site.register(Evento)