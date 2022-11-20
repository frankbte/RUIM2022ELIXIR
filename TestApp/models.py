from django.db import models
from django.forms import ModelForm
from django.core.validators import FileExtensionValidator

class PresentacionRegistro(models.Model):
    modalidadChoices = (
        ('Cartel','Cartel'),
        ('Ponencia','Ponencia'),
    )
    estatusChoices = (
        ('Sin revisar','Sin revisar'),
        ('Aceptado', 'Aceptado'),
        ('Rechazado', 'Rechazado')
    )
    presentacion_titulo = models.CharField(max_length = 40, verbose_name="Título de la presentación")
    resp = models.ForeignKey('Author',related_name = "resp", on_delete = models.CASCADE, default = '', blank=True,null=True)
    resp_email = models.EmailField()
    modalidad = models.CharField(max_length = 30, choices=modalidadChoices) # cartel o ponencia
    resumen = models.FileField(upload_to = 'registros/resumenes/', validators = [FileExtensionValidator(allowed_extensions = ['pdf'])])
    estatus = models.CharField(max_length = 30, choices=estatusChoices)
    evento = models.ForeignKey('Evento', on_delete = models.CASCADE,)
    
class Author(models.Model):
    gradoChoices = (
        ('Estudiante','Estudiante'),
        ('Ingeniería', 'Ingeniería'),
        ('Licenciatura', 'Licenciatura'),
        ('Doctorado', 'Doctorado'),
        ('Maestría', 'Maestría')
    )
    nombre = models.CharField(max_length = 20)
    apellido_pat = models.CharField(max_length = 20)
    apellido_mat = models.CharField(max_length = 20)
    grado = models.CharField(max_length = 30, choices=gradoChoices)
    institucion = models.CharField(max_length = 60)
    departamento = models.CharField(max_length = 40)
    presentacion = models.ForeignKey('PresentacionRegistro', on_delete = models.CASCADE, default = '')

class InicioPage(models.Model):
    title_descripcion = models.CharField(max_length = 40)
    text_descripcion = models.CharField(max_length = 300)

class ProgramaPage(models.Model):
    programa_pdf = models.FileField(upload_to = 'admin/')
    programa_img = models.ImageField(upload_to = 'admin/')

class PosterPage(models.Model):
    poster_img = models.ImageField(upload_to = 'admin/')
    poster_pdf = models.FileField(upload_to = 'admin/')

class RegistroPage(models.Model):
    title_participacion_ponente = models.CharField(max_length = 40)
    text_participacion_ponente = models.CharField(max_length = 300)
    title_formato_resumen = models.CharField(max_length = 40)
    text_formato_resumen = models.CharField(max_length = 300)
    title_constancias_participacion = models.CharField(max_length = 40)
    text_constancias_participacion = models.CharField(max_length = 300)
    title_participacion_asistente = models.CharField(max_length = 40)
    text_participacion_asistente = models.CharField(max_length = 300)
    formato_resumen_pdf = models.FileField(upload_to = 'admin/')


class UbicacionPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    url_maps_embed = models.CharField(max_length = 500)
    url_maps = models.URLField(max_length = 200)

class ContactoPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    contacto = models.CharField(max_length = 30)

class EdicionesPage(models.Model):
    title = models.CharField(max_length = 40)
    text = models.CharField(max_length = 300)
    

class Evento(models.Model):
    active = models.BooleanField()
    editing = models.BooleanField()
    year = models.IntegerField(default=2022)
    cartel = models.FileField(upload_to = 'admin/', blank=True,null=True)
    inicio = models.ForeignKey('InicioPage', on_delete = models.CASCADE, blank=True,null=True)
    programa = models.ForeignKey('ProgramaPage', on_delete = models.CASCADE, blank=True,null=True)
    poster = models.ForeignKey('PosterPage', on_delete = models.CASCADE, blank=True,null=True)
    ubicacion = models.ForeignKey('UbicacionPage', on_delete = models.CASCADE, blank=True,null=True)
    contacto = models.ForeignKey('ContactoPage', on_delete = models.CASCADE, blank=True,null=True)
    registro = models.ForeignKey('RegistroPage', on_delete = models.CASCADE, blank=True,null=True)
    edicion = models.ForeignKey('EdicionesPage', on_delete = models.CASCADE,blank=True,null=True)
    plantilla_constancias_img = models.ImageField(upload_to = 'admin/', blank=True,null=True)    # Imagen tamaño Letter
    correo_comunicacion = models.EmailField(blank=True,null=True)
    correo_contrasena = models.CharField(max_length = 100, blank=True,null=True)
    fecha = models.DateField()
    lugar = models.CharField(max_length=100)

    def save_all(self):
        self.inicio.save()
        self.programa.save()
        self.poster.save()
        self.ubicacion.save()
        self.contacto.save()
        self.registro.save()
        self.edicion.save()
        return 0


DEFAULT_EVENT = Evento(active = False, year = 2022, editing = False, \
                        inicio = InicioPage(title_descripcion = "RUIM 2022", \
                                text_descripcion = "El objetivo de la Reunión Universitaria de Investigación en Materiales (RUIM 2022) es dar a conocer a la comunidad universitaria las actividades que se desarrollan en nuestra institución mediante la presentación de trabajos, por parte de estudiantes y profesores de la Universidad de Sonora, que tengan como temática la investigación en materiales. \
    \n\n Por lo anterior, se convoca a los estudiantes de Posgrado y estudiantes avanzados de Licenciatura, así como a los profesores e investigadores de las Divisiones de Ciencias Exactas y Naturales (DCEN), Ciencias Biológicas y de la Salud (DCBS), e Ingeniería (DI) de la Universidad de Sonora, a presentar trabajos en la XXV Reunión Universitaria de Investigación en Materiales (RUIM 2022)."), \
                        programa = ProgramaPage(programa_pdf = "archivos/admin/programa.pdf", programa_img = "archivos/admin/programa.jpg"), \
                        poster = PosterPage(poster_pdf = "archivos/admin/poster.pdf", poster_img = "archivos/admin/poster.jpg"), \
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
                        edicion = EdicionesPage(title = "Ediciones anteriores de la RUIM:", text = ""),
                        registro = RegistroPage(title_participacion_ponente = "Participación como ponente",
                                                text_participacion_ponente = "Las formas de Participación en la RUIM 2022 son las siguientes: \n\n - Pláticas Invitadas\n - Posters.\n",
                                                title_formato_resumen = "Formato para Resumen",
                                                text_formato_resumen = "El formato del Resumen es igual para las dos formas de participación y la extensión es de una o dos cuartillas siguiendo la plantilla en formato Word 2010 y posteriores (*.docx), la cual está disponible en esta página",
                                                title_constancias_participacion = "Constancias de participación",
                                                text_constancias_participacion = "Se extenderán Constancias de Participación en los siguientes formatos: \n\n - Plática Invitada (Constancias de Plática Invitada);\n - Poster (Constancia de Presentación de Cartel).\n",
                                                title_participacion_asistente = "Participacición en los Cursos Talleres",
                                                text_participacion_asistente = "Para participar en alguno de los Cursos-Talleres que se realizarán durante la RUIM 2022, se hace necesario pre-registrarse, para ello, próximamente se habilitará el enlace correspondiente",
                                                formato_resumen_pdf = "archivos/registros/resumenes/RUIM2022.docx"),
                        fecha = "2022-11-12",
                        lugar = "Hermosillo, Sonora")




