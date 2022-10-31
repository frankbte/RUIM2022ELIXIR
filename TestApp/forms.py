from django import forms  
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro

class EventoForm(forms.ModelForm):  
    class Meta:  
        model = Evento
        fields = "__all__"

class PresentacionForm(forms.ModelForm):
    class Meta:
        model = PresentacionRegistro
        fields = [
            'presentacion_titulo', 
            'resp',
            'resp_email',
            'a1',
            'a2',
            'a3',
            'a4',
            'a5',
            'a6',
            'a7',
            'institucion',
            'departamento',
            'modalidad',
            'resumen'
            ]

        labels = {
            'presentacion_titulo': 'Titulo de la presentación',
            'resp': 'Responsable de la presentación',
            'resp_email': 'Correo electrónico del representante de la presentación',
            'a1': 'Autor 1',
            'a2': 'Autor 2',
            'a3': 'Autor 3',
            'a4': 'Autor 4',
            'a5': 'Autor 5',
            'a6': 'Autor 6',
            'a7': 'Autor 7',
            'institucion': 'Institución de procedencia',
            'departamento': 'Departamento',
            'modalidad': 'Tipo de presentación (ponencia o cartel)',
            'resumen': 'Breve resumen de la presentación (archivo PDF)'
        }

class InicioPageForm(forms.ModelForm):
    class Meta:
        model = InicioPage
        fields = ['title_descripcion', 'text_descripcion']
        labels = {'title_descripcion' : 'Descripción del evento', 'text_descripcion' : 'Encabezado de la pestaña'}

class ContactoPageForm(forms.ModelForm):
    class Meta:
        model = ContactoPage
        fields = ['title', 'text', 'contacto']
        labels = {'title' : 'Encabezado de la pestaña', 'text' : 'Mensaje', 'contacto' : 'Correo electrónico de contacto'}


