from django.db import models

class Presentacion(models.Model):
    presentacion_titulo = models.CharField(max_length = 40)
    resp_nombre = models.CharField(max_length = 20)
    resp_apellido_pat = models.CharField(max_length = 20)
    resp_apellido_mat = models.CharField(max_length = 20)
    email = models.EmailField()
    institucion = models.CharField(max_length = 40)
    departamento = models.CharField(max_length = 40)
    grado = models.CharField(max_length = 30)
    modalidad = models.CharField(max_length = 30)
    titulo = models.CharField()
    autores = models.CharField()
    resumen = models.FileField(upload_to = 'registros/resumenes/')
    constancia = models.Filefield(upload_to = 'registros/constanciaas/')
    estatus = models.CharField(max_length = 30)

class Inicio(models.Model):
    titulo = models.CharField(max_length = 40)
    descripcion = models.CharField()
    link_texto = models.URLField()
    link_url = models.URLField()

class Programa(models.Model):
    titulo = models.CharField(max_length = 40)
    pdf = models.Filefield(upload_to = 'programa/')

class Poster(models.Model):
    titulo = models.CharField(max_length = 40)
    poster = models.ImageField()

class Registro(models.Model):
    titulo = models.CharField(max_length = 40)
    mensaje = models.CharField()
    link_resumen = models.FileField(upload_to = 'registros/resumenes/')
    descripcion = models.CharField()

class Ubicacion(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField()
    widget = models.URLField()

class Contacto(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField()
    contacto = models.CharField()

class Edicion(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField()

class PlantillaBase(models.Model):
    cartel = models.FileField(upload_to = 'base/')
    titulo = models.CharField(max_length = 40)
    pie_texto = models.CharField()
    link_texto = models.CharField(max_length = 40)
    link_url = models.URLField()

class IterAnteriores(models.Model):
    titulo = models.CharField(max_length = 60)
    texto = models.CharField()

    def get_events():
        return Evento.objects.all()

class Evento(models.Model):
    nombre_evento = CharField()
    inicio = models.ForeignKey('Inicio', on_delete = models.CASACADE,)
    programa = models.ForeignKey('Programa', on_delete = models.CASACADE,)
    poster = models.ForeignKey('Poster', on_delete = models.CASACADE,)
    ubicacion = models.ForeignKey('Ubicacion', on_delete = models.CASACADE,)
    contacto = models.ForeignKey('Contacto', on_delete = models.CASACADE,)
    registro = models.ForeignKey('Registro', on_delete = models.CASACADE,)
    anteriores = models.ForeignKey('IterAnteriores', on_delete = models.CASACADE,)
    base = models.ForeignKey('PlantillaBase', on_delete = models.CASACADE,)
    plantilla_constancias = models.FileField(upload_to = 'constancias/base/')
    correo_comunicacion = models.EmailField()
    correo_contrasena = models.CharField()




