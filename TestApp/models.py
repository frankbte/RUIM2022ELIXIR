from django.db import models

class Presentacion(models.Model):
    presentacion_titulo = models.CharField()
    resp_nombre = models.CharField()
    resp_apellido_pat = models.CharField()
    resp_apellido_mat = models.CharField()
    email = models.EmailField()
    institucion = models.CharField()
    departamento = models.CharField()
    grado = models.TextChoices()
    modalidad = models.TextChoices()
    edicion = models.DateField()
    estatus = models.TextChoices()

class Inicio(models.Model):
    titulo = models.CharField()
    descripcion = models.CharField()
    link_texto = models.URLField()
    link_url = models.URLField()

class Programa(models.Model):
    titulo = models.CharField()
    pdf = models.CharField()

class Poster(models.Model):
    titulo = models.CharField()
    poster = models.ImageField()

class Registro(models.Model):
    titulo = models.CharField()
    mensaje = models.CharField()
    link_resumen = models.URLField()

class Ubicacion(models.Model):
    titulo = models.CharField()
    texto = models.CharField()
    widget = models.URLField()

class Contacto(models.Model):
    titulo = models.CharField()
    texto = models.CharField()
    contacto = models.CharField()

class Edicion(models.Model):
    titulo = models.CharField()
    texto = models.CharField()

class PlantillaBase(models.Model):
    cartel = models.URLField()
    titulo = models.CharField()
    pie_texto = models.CharField()
    link_texto = models.CharField()
    link_url = models.URLField()
