from django.shortcuts import render, redirect
from django.db import models
from TestApp.forms import AuthorForm, EventoForm, InicioPageForm, ContactoPageForm, PresentacionForm
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro, Author, DEFAULT_EVENT
from TestApp import urls
from django.http import FileResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, BadHeaderError, send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
    
from fpdf import FPDF

def home(request):
    return render(request, 'TestApp/home.html', {'home' : get_current_event().inicio})

def programa(request):
    return render(request, 'TestApp/programa.html', 
            {'programa' : get_current_event().programa})

def poster(request):
    return render(request, 'TestApp/poster.html', 
            {'poster' : get_current_event().poster})

def ubicacion(request):
    return render(request, 'TestApp/ubicacion.html', 
            {'ubicacion' : get_current_event().ubicacion})


def contacto(request):
    return render(request, 'TestApp/contacto.html', 
            {'contacto' : get_current_event().contacto})


def ponencias(request):
        pform = PresentacionForm()
        aform = AuthorForm()
        return render(request, 'TestApp/ponencias.html', 
                      {'pform': pform, 
                       'aform': aform,
                       'registro': get_current_event().registro})

def ediciones(request):
    return render(request, 'TestApp/ediciones.html', 
            {'edicion' : get_current_event().edicion})


# Vistas de administrador

def administrador_redirect_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("TestApp:Edicion_Iteraciones"))

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


@login_required
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
def create_iter(request):
    return render(request, 'TestApp/AdminFront/creacionIteracion.html')


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

def AddPresentation(request):
    presentacion = PresentacionRegistro(presentacion_titulo=request.GET["pres_tit"],
                                        resp_email=request.GET["pres_email"],
                                        modalidad=request.GET["mod"],
                                        estatus="Sin revisar",
                                        evento=Evento.objects.filter(active=True).get())

    presentacion.save()

    responsable = Author(   nombre=request.GET["resp_nom"],
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
        for x in range(1,cant_auth+1):
            autor = Author( nombre=request.GET["a" + str(x) + "_nom"],
                            apellido_pat=request.GET["a" + str(x) + "_pat"],
                            apellido_mat=request.GET["a" + str(x) + "_mat"],
                            institucion=request.GET["a" + str(x) + "_inst"],
                            departamento=request.GET["a" + str(x) + "_dep"],
                            grado=request.GET["a" + str(x) + "_grado"],
                            presentacion=presentacion)
            autor.save()

    presentacion.save()

    return render(request, "TestApp/ponencias.html")

###########################
# Controladores

@login_required
def insert_iter(request):
    year = request.POST.get("year")
    cartel = request.POST.get("cartel")
    correo = request.POST.get("correo")
    correo_contrasena = request.POST.get("correo_contrasena")
    fecha = request.POST.get("date")
    lugar = request.POST.get("place")
    plantilla_constancias = request.POST.get("plantilla_constancias")

    new_event = Evento()
    new_event.active = False
    new_event.year = year
    new_event.cartel = cartel
    new_event.correo_comunicacion = correo
    new_event.correo_contrasena = correo_contrasena
    new_event.fecha = fecha
    new_event.lugar = lugar
    new_event.plantilla_constancias_img = plantilla_constancias

    new_event.inicio = DEFAULT_EVENT.inicio
    new_event.programa = DEFAULT_EVENT.programa
    new_event.poster = DEFAULT_EVENT.poster
    new_event.ubicacion = DEFAULT_EVENT.ubicacion
    new_event.contacto = DEFAULT_EVENT.contacto
    new_event.registro = DEFAULT_EVENT.registro
    new_event.edicion = DEFAULT_EVENT.edicion
    new_event.contacto = DEFAULT_EVENT.contacto

    try:
        new_event.save_all()
        new_event.save() 
        request.session["success_message"] = "Evento nuevo creado con información default para vistas de usuario."

    except Evento.DoesNotExist:
        request.session["seccess_message"] = "No se pudo crear el evento!"

    return redirect(reverse('TestApp:Edicion Iteraciones')) 
    

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


def get_current_event():
    eventos = Evento.objects.all()

    if eventos.count() > 0:
        eventos = eventos.filter(active = True)
        if eventos.count() > 0:
            return eventos[0]

    return DEFAULT_EVENT

