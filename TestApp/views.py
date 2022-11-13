from django.shortcuts import render, redirect
from django.db import models
from TestApp.forms import AuthorForm, EventoForm, InicioPageForm, ContactoPageForm, PresentacionForm
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro, Author
from TestApp import urls
from django.http import FileResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError, send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
    
from fpdf import FPDF

def home(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        home = current_events[0].inicio
        return render(request, 'TestApp/home.html', {'home' : home})

    return render(request, 'TestApp/home.html')

def programa(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        programa = current_events[0].programa
        return render(request, 'TestApp/programa.html', {'programa' : programa})

    return render(request, 'TestApp/programa.html')

def poster(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        poster = current_events[0].poster
        return render(request, 'TestApp/poster.html', {'poster' : poster})

    return render(request, 'TestApp/poster.html')

def ubicacion(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        ubicacion = current_events[0].ubicacion
        return render(request, 'TestApp/ubicacion.html', {'ubicacion' : ubicacion})

    return render(request, 'TestApp/ubicacion.html')

def contacto(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        contacto = current_events[0].contacto
        return render(request, 'TestApp/contacto.html', {'contacto' : contacto})

    return render(request, 'TestApp/contacto.html')

def ponencias(request):
        pform = PresentacionForm()
        aform = AuthorForm()
        return render(request, 'TestApp/ponencias.html', 
                      {'pform': pform, 
                       'aform': aform})

def ediciones(request):
    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        edicion = current_events[0].edicion
        return render(request, 'TestApp/ediciones.html', {'' : edicion})

    return render(request, 'TestApp/ediciones.html')

# Vistas de administrador

def administrador_redirect_login(request):
    return HttpResponseRedirect(reverse("TestApp:login"))

@login_required
def baseFront(request):
    return render(request, 'TestApp/AdminFront/baseAdmin.html')

@login_required
def evento(request):
    return render(request, 'TestApp/evento.html')

@login_required
def constancias(request):
    return render(request, 'TestApp/AdminFront/constancias.html')


@login_required
def correos(request):
    return render(request, 'TestApp/AdminFront/correos.html')


def iterAdmin(request):
    eventos = Evento.objects.all()
    
    message = request.session.get("success_message", "")
    request.session["success_message"] = ""
        
    if Evento.objects.count() > 0:
        if Evento.objects.filter(active = 1).count() == 1:
            current_event = Evento.objects.get(active = 1)
            return render(request, 'TestApp/AdminFront/edicionesFront.html', {'iteracion' : current_event, 'iteracion_list' : eventos, 'message' : message})
            
        return render(request, 'TestApp/AdminFront/edicionesFront.html', {'iteracion_list' : eventos, 'message' : message})
    
    return render(request, 'TestApp/AdminFront/edicionesFront.html', {'message' : message})

@login_required
def informe(request):
    return render(request, 'TestApp/AdminFront/informe.html')

@login_required
def inicioAdmin(request):
    form = InicioPageForm()
    return render(request, 'TestApp/AdminFront/inicioAdmin.html', {'form': form})

@login_required
def contactoAdmin(request):
    form = ContactoPageForm()
    return render(request, 'TestApp/AdminFront/contactoAdmin.html', {'form': form})

############################
# COSAS DE ERICK, NO TOCAR #
############################
#def FormPage(request):
#    return render(request, "TestApp/AdminFront/form.html")

def ResultPage(request):
    results = PresentacionRegistro.objects.filter()
    return render(request, "TestApp/AdminFront/results.html",{"results":results})

def AddPresentation(request):
    presentacion = PresentacionRegistro(presentacion_titulo=request.GET["pres_tit"],
                                        resp_email=request.GET["pres_email"],
                                        modalidad=request.GET["mod"],
                                        estatus="Sin revisar",
                                        evento=Evento.objects.get())

    presentacion.save()

    responsable = Author(nombre=request.GET["resp_nom"],
                        apellido_pat=request.GET["resp_pat"],
                        apellido_mat=request.GET["resp_mat"],
                        institucion=request.GET["resp_inst"],
                        departamento=request.GET["resp_dep"],
                        grado=request.GET["resp_grado"],
                        presentacion=presentacion)

    responsable.save()
    
    presentacion.resp = responsable

    cant_auth=int(request.GET["cant_auth"])
    if cant_auth > 0:
        for x in range(cant_auth):
            autor = Author(nombre=request.GET["a" + x + "_nom"],
                            apellido_pat=request.GET["a" + x + "_pat"],
                            apellido_mat=request.GET["a" + x + "_mat"],
                            institucion=request.GET["a" + x + "_inst"],
                            departamento=request.GET["a" + x + "_dep"],
                            grado=request.GET["a" + x + "_grado"],
                            presentacion=presentacion)
            autor.save()

    presentacion.save()

    return render(request, "TestApp/ponencias.html")

def delete(request):
    congresos = PresentacionRegistro.objects.filter()
    congresos.delete()
    return render(request, "form.html")

###########################
# Controladores

def report(request):
    font = 'times'
    size = 20
    height = 12
    
    pdf = FPDF('L', 'mm', 'letter')
    pdf.set_text_color(0,0,0)
    
    pdf.add_page()
    pdf.image('TestApp\static\TestApp\img\Certificado.jpg', x=0, y=0, w=280, h=216)
    pdf.image('TestApp\static\TestApp\img\Escudo_Unison.png', x=15, y=7, w=35, h=40)
    pdf.set_font(font, '', size)
    pos = pdf.get_y() + 40
    
    pdf.set_xy(10, pos)
    pdf.multi_cell(w = 0, h = height, txt= 'La Reunion Universitaria de Investigación en Materiales otorga el presente', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10, pos)
    pdf.set_font(font, 'B', size + 8)
    pdf.multi_cell(w = 0, h = height, txt= 'RECONOCIMIENTO', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10, pos)
    pdf.set_font(font, '', size)
    pdf.multi_cell(w = 0, h = height, txt= 'a:', border = 0 ,align ='l')
    pdf.set_xy(15,pos)
    pdf.set_font(font, 'I', size)
    pdf.multi_cell(w = 0, h = height, txt= '___________________________', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, '', size)
    pdf.multi_cell(w = 0, h = height, txt= 'Por haber asistido y presentado su _______ con título', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, 'I', size)
    pdf.multi_cell(w = 0, h = height, txt= ' ____________________________________', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, '', size)
    pdf.multi_cell(w = 0, h = height, txt= 'el día ________ en ____________________', border = 0 ,align ='c')
    pdf.output('report.pdf', 'F')
    
    return FileResponse(open('report.pdf', 'rb'), as_attachment=True, content_type='application/pdf')



def remove_iteration(request):
    event_year = request.POST.get("eliminar") #Desde el view, la seleccion de evento es a trav\'es del a\~no.

    try:
        event = Evento.objects.get(year = event_year)
        event.delete()
        request.session["success_message"] = "Evento eliminado!"

    except Evento.DoesNotExist:
        request.session["seccess_message"] = "Ha ocurrido un error!"

    return redirect(reverse('TestApp:Edicion Iteraciones')) 


def send_email(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    to_email = request.POST.get('to_email')
    
    try:
        send_mail(subject, message, 'RUinvestigacionmateriales@outlook.com', [to_email],)
    except BadHeaderError:
        return render(request, "TestApp/AdminFront/correos.html", { "message" : "Invalid Header Found" })
    return render(request, "TestApp/AdminFront/correos.html", { "message" : "Envío de correo exitoso" })



