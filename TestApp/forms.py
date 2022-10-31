from django import forms  
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro

class EventoForm(forms.ModelForm):  
    class Meta:  
        model = Evento
        fields = "__all__"

class PresentacionForm(forms.ModelForm):
    class Meta:
        model = PresentacionRegistro
        fields = "__all__"

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


