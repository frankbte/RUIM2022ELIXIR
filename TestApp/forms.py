from telnetlib import AUTHENTICATION
from django import forms  
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro, Author, UbicacionPage, PosterPage, ProgramaPage, RegistroPage
from django.forms import Textarea, FileInput

class EventoForm(forms.ModelForm):  
    class Meta:  
        model = Evento
        fields = "__all__"
        
class AuthorForm(forms.ModelForm):  
    class Meta:  
        model = Author
        fields = ['nombre', 'apellido_pat', 'apellido_mat', 'institucion', 'departamento']
        labels = {'nombre' : 'Nombre',
                  'apellido_pat' : 'Apellido Paterno',
                  'apellido_mat' : 'Apellido Materno',
                  'institucion' : 'Institución',
                  'departamento' : 'Departamento/Facultad'}


class PresentacionForm(forms.ModelForm):
    class Meta:
        model = PresentacionRegistro
        fields = [
            'presentacion_titulo', 
            'resp',
            'resp_email',
            'modalidad',
            'resumen'
            ]

        labels = {
            'presentacion_titulo': 'Titulo de la presentación',
            'resp': 'Responsable de la presentación',
            'resp_email': 'Correo electrónico del representante de la presentación',
            'modalidad': 'Tipo de presentación (ponencia o cartel)',
            'resumen': 'Breve resumen de la presentación (archivo PDF)'
        }

class InicioPageForm(forms.ModelForm):
    class Meta:
        model = InicioPage
        fields = "__all__"
        labels = {'title_descripcion' : 'Título para descripción del evento', 'text_descripcion' : 'Texto para descripción del evento',
                  'title_news' : 'Título para noticias (opcional)', 'text_news' : 'Texto para noticias (opcional)', 'cartel' : 'Banner del inicio (imagen)'}
        widgets = {'text_descripcion': Textarea, 'text_news': Textarea,}

class ContactoPageForm(forms.ModelForm):
    class Meta:
        model = ContactoPage
        fields = ['title', 'text', 'contacto']
        labels = {'title' : 'Encabezado de la pestaña', 'text' : 'Mensaje', 'contacto' : 'Correo electrónico de contacto'}
        widgets = {'text' : Textarea(attrs={'rows': 2})}


class UbicacionPageForm(forms.ModelForm):  
    class Meta:  
        model = UbicacionPage
        fields = "__all__"
        labels = {'title' : 'Encabezado de la pestaña',
                  'text' : 'Mensaje',
                  'url_maps' : 'URL de maps',
                  'url_maps_embed' : 'URL del embed de maps'}
        widgets = {'text' : Textarea(attrs={'rows': 4})}

class PosterPageForm(forms.ModelForm):  
    class Meta:  
        model = PosterPage
        fields = "__all__"
        labels = {'poster_img' : 'Imagen del poster',
                  'poster_pdf' : 'PDF del poster'}
        
class ProgramaPageForm(forms.ModelForm):  
    class Meta:  
        model = ProgramaPage
        fields = "__all__"
        labels = {'programa_img' : 'Imagen del Programa',
                  'programa_pdf' : 'PDF del programa'}
        widgets = {'programa_img': FileInput(attrs={'accept':'.jpg, .jpeg'}),
                   'programa_pdf' : FileInput(attrs={'accpet':'.pdf'}), }

class RegistroPageForm(forms.ModelForm):  
    class Meta:  
        model = RegistroPage
        fields = "__all__"
        labels = {'title_participacion_ponente' : 'Título para participación del ponente',
                  'text_participacion_ponente' : 'Texto para participación del ponente',
                  'title_formato_resumen' : 'Título para formato del resumen',
                  'text_formato_resumen' : 'Texto para formato del resumen',
                  'title_constancias_participacion' : 'Título para entrega de constancias ',
                  'text_constancias_participacion' : 'Texto para entrega de constancias ',
                  'title_participacion_asistente' : 'Título para participación del asistente',
                  'text_participacion_asistente' : 'Texto para participación del asistente'}        
        widgets = {'text_participacion_ponente' : Textarea(attrs={'rows': 3}),
                'text_formato_resumen' : Textarea(attrs={'rows': 3}),
                'text_constancias_participacion' : Textarea(attrs={'rows': 3}),
                'text_participacion_asistente' : Textarea(attrs={'rows': 3}),}
