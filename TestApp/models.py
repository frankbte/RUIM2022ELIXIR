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
    titulo = models.CharField(max_length = 70)
    autores = models.CharField(max_length = 300)
    resumen = models.FileField(upload_to = 'registros/resumenes/')
    constancia = models.FileField(upload_to = 'registros/constanciaas/')
    estatus = models.CharField(max_length = 30)

class Inicio(models.Model):
    titulo = models.CharField(max_length = 40)
    descripcion = models.CharField(max_length = 300)
    link_texto = models.URLField(max_length = 70)
    link_url = models.URLField(max_length = 70)

class Programa(models.Model):
    titulo = models.CharField(max_length = 40)
    pdf = models.FileField(upload_to = 'programa/')

class Poster(models.Model):
    titulo = models.CharField(max_length = 40)
    poster = models.ImageField()

class Registro(models.Model):
    titulo = models.CharField(max_length = 40)
    mensaje = models.CharField(max_length = 300)
    link_resumen = models.FileField(upload_to = 'registros/resumenes/')
    descripcion = models.CharField(max_length = 300)

class Ubicacion(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField(max_length = 300)
    widget = models.URLField(max_length = 70)

class Contacto(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField(max_length = 300)
    contacto = models.CharField(max_length = 30)

class Edicion(models.Model):
    titulo = models.CharField(max_length = 40)
    texto = models.CharField(max_length = 300)

class PlantillaBase(models.Model):
    cartel = models.FileField(upload_to = 'base/')
    titulo = models.CharField(max_length = 40)
    pie_texto = models.CharField(max_length = 40)
    link_texto = models.CharField(max_length = 40)
    link_url = models.URLField()

class IterAnteriores(models.Model):
    titulo = models.CharField(max_length = 60)
    texto = models.CharField(max_length = 300)

    def get_events():
        return Evento.objects.all()

class Evento(models.Model):
    nombre_evento = models.CharField(max_length = 70)
    inicio = models.ForeignKey('Inicio', on_delete = models.CASCADE,)
    programa = models.ForeignKey('Programa', on_delete = models.CASCADE,)
    poster = models.ForeignKey('Poster', on_delete = models.CASCADE,)
    ubicacion = models.ForeignKey('Ubicacion', on_delete = models.CASCADE,)
    contacto = models.ForeignKey('Contacto', on_delete = models.CASCADE,)
    registro = models.ForeignKey('Registro', on_delete = models.CASCADE,)
    anteriores = models.ForeignKey('IterAnteriores', on_delete = models.CASCADE,)
    base = models.ForeignKey('PlantillaBase', on_delete = models.CASCADE,)
    plantilla_constancias = models.FileField(upload_to = 'constancias/base/')
    correo_comunicacion = models.EmailField()
    correo_contrasena = models.CharField(max_length = 100)




