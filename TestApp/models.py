from django.db import models

class Presentacion(models.Model):
    presentacion_titulo = models.CharField(max_length = 40)
    resp_nombre = models.CharField(max_length = 20)
    resp_apellido_pat = models.CharField(max_length = 20)
    resp_apellido_mat = models.CharField(max_length = 20)
    email = models.EmailField()
    institucion = models.CharField(max_length = 40)
    departamento = models.CharField(max_length = 40)
    grado = models.TextChoices()
    modalidad = models.TextChoices()
    edicion = models.DateField()
    estatus = models.TextChoices()

class Inicio(models.Model):
    titulo = models.CharField(max_length = 40)
    descripcion = models.CharField()
    link_texto = models.URLField()
    link_url = models.URLField()

class Programa(models.Model):
    titulo = models.CharField(max_length = 40)
    pdf = models.CharField()

class Poster(models.Model):
    titulo = models.CharField(max_length = 40)
    poster = models.ImageField()

class Registro(models.Model):
    titulo = models.CharField(max_length = 40)
    mensaje = models.CharField()
    link_resumen = models.URLField()

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
    cartel = models.URLField()
    titulo = models.CharField(max_length = 40)
    pie_texto = models.CharField()
    link_texto = models.CharField(max_length = 40)
    link_url = models.URLField()

class Edicion(models.Model):
    titulo = models.CharField()
    texto = models.CharField()

class PlantillaBase(models.Model):
    cartel = models.URLField()
    titulo = models.CharField()
    pie_texto = models.CharField()
    link_texto = models.CharField()
    link_url = models.URLField()
