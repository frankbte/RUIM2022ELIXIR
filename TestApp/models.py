from django.db import models
from django.forms import ModelForm

class PresentacionRegistro(models.Model):
    presentacion_titulo = models.CharField(max_length = 40)
    resp = models.ForeignKey('Author',related_name = "resp", on_delete = models.CASCADE, default = '')
    resp_email = models.EmailField()
    a1 = models.ForeignKey('Author', related_name = "a1", on_delete = models.CASCADE, blank=True,null=True)
    a2 = models.ForeignKey('Author', related_name = "a2", on_delete = models.CASCADE, blank=True,null=True)
    a3 = models.ForeignKey('Author', related_name = "a3", on_delete = models.CASCADE, blank=True,null=True)
    a4 = models.ForeignKey('Author', related_name = "a4", on_delete = models.CASCADE, blank=True,null=True)
    a5 = models.ForeignKey('Author', related_name = "a5", on_delete = models.CASCADE, blank=True,null=True)
    a6 = models.ForeignKey('Author', related_name = "a6", on_delete = models.CASCADE, blank=True,null=True)
    a7 = models.ForeignKey('Author', related_name = "a7", on_delete = models.CASCADE, blank=True,null=True)
    institucion = models.CharField(max_length = 60)
    departamento = models.CharField(max_length = 40)
    modalidad = models.CharField(max_length = 30) # cartel o ponencia
    resumen = models.FileField(upload_to = 'registros/resumenes/')
    estatus = models.CharField(max_length = 30)
    evento = models.ForeignKey('Evento', on_delete = models.CASCADE,)
    
class Author(models.Model):
    nombre = models.CharField(max_length = 20)
    apellido_pat = models.CharField(max_length = 20)
    apellido_mat = models.CharField(max_length = 20)
    grado = models.CharField(max_length = 30)

class InicioPage(models.Model):
    title_descripcion = models.CharField(max_length = 40)
    text_descripcion = models.CharField(max_length = 300)

class ProgramaPage(models.Model):
    title = models.CharField(max_length = 40)
    programa_pdf = models.FileField(upload_to = 'TestApp/static/TestApp/archivos/')
    programa_img = models.ImageField(upload_to = 'archivos/')

class PosterPage(models.Model):
    title = models.CharField(max_length = 40)
    poster_img = models.ImageField(upload_to = 'archivos/')

class RegistroPage(models.Model):
    title_participacion_ponente = models.CharField(max_length = 40)
    text_participacion_ponente = models.CharField(max_length = 300)
    title_formato_resumen = models.CharField(max_length = 40)
    text_formato_resumen = models.CharField(max_length = 300)
    title_constancias_participacion = models.CharField(max_length = 40)
    text_constancias_participacion = models.CharField(max_length = 300)
    title_participacion_asistente = models.CharField(max_length = 40)
    text_participacion_asistente = models.CharField(max_length = 300)
    formato_resumen_pdf = models.FileField(upload_to = 'registros/resumenes/')

class UbicacionPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    url_maps_embed = models.URLField(max_length = 250)
    url_maps = models.URLField(max_length = 200)

class ContactoPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    contacto = models.CharField(max_length = 30)

class EdicionesPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    

class Evento(models.Model):
    active = models.IntegerField()
    year = models.IntegerField()
    cartel = models.FileField(upload_to = 'base/', blank=True,null=True)
    inicio = models.ForeignKey('InicioPage', on_delete = models.CASCADE, blank=True,null=True)
    programa = models.ForeignKey('ProgramaPage', on_delete = models.CASCADE, blank=True,null=True)
    poster = models.ForeignKey('PosterPage', on_delete = models.CASCADE, blank=True,null=True)
    ubicacion = models.ForeignKey('UbicacionPage', on_delete = models.CASCADE, blank=True,null=True)
    contacto = models.ForeignKey('ContactoPage', on_delete = models.CASCADE, blank=True,null=True)
    registro = models.ForeignKey('RegistroPage', on_delete = models.CASCADE, blank=True,null=True)
    edicion = models.ForeignKey('EdicionesPage', on_delete = models.CASCADE,blank=True,null=True)
    plantilla_constancias_img = models.ImageField(upload_to = 'constancias/base/', blank=True,null=True)    # Imagen tamaño Letter (216 x 280 mm)
    correo_comunicacion = models.EmailField(blank=True,null=True)
    correo_contrasena = models.CharField(max_length = 100, blank=True,null=True)

    def save_all(self):
        self.inicio.save()
        self.programa.save()
        self.poster.save()
        self.ubicacion.save()
        self.contacto.save()
        #self.registro.save()
        self.edicion.save()
        return 0


DEFAULT_EVENT = Evento(active = 0, year = 2022, \
                        inicio = InicioPage(title_descripcion = "RUIM 2022", \
                                text_descripcion = "El objetivo de la Reunión Universitaria de Investigación en Materiales (RUIM 2022) es dar a conocer a la comunidad universitaria las actividades que se desarrollan en nuestra institución mediante la presentación de trabajos, por parte de estudiantes y profesores de la Universidad de Sonora, que tengan como temática la investigación en materiales. \
    \n\n Por lo anterior, se convoca a los estudiantes de Posgrado y estudiantes avanzados de Licenciatura, así como a los profesores e investigadores de las Divisiones de Ciencias Exactas y Naturales (DCEN), Ciencias Biológicas y de la Salud (DCBS), e Ingeniería (DI) de la Universidad de Sonora, a presentar trabajos en la XXV Reunión Universitaria de Investigación en Materiales (RUIM 2022)."), \
                        programa = ProgramaPage(title = "Congreso RUIM", programa_pdf = "archivos/programa.pdf"), \
                        poster = PosterPage(title = "RUIM 2022", poster_img = "archivos/poster.jpg"), \
                        ubicacion = UbicacionPage(title = "RUIM 2022", \
                                                    text = "Centro de las Artes de la Universidad de Sonora \n \
                                                    Ubicado en: Blvd. Luis Donaldo Colosio y Rosales S/N  \n \
                                                    Colonia Centro  \n \
                                                    Hermosillo, Sonora \n", \
                                                    url_maps_embed = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3486.814738923721!2d-110.96154618495328!3d29.081618982242823!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x86ce84491ead1bcf%3A0xfdb274fba98a7049!2sCentro%20de%20las%20Artes%20Unison!5e0!3m2!1ses!2smx!4v1666635438505!5m2!1ses!2smx", \
                                                    url_maps = "https://goo.gl/maps/muocjqEYp8YSUs1p6"), \
                        contacto = ContactoPage(title = "RUIM 2022", \
                                                text = "Para cualquier duda o comentario, ponemos a su disposición \n la siguiente dirección de correo electrónico: \n", \
                                                contacto = "ruim@unison.mx"), \
                        edicion = EdicionesPage(title = "Ediciones anteriores de la RUIM:", text = ""))



