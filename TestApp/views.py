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
import re
    
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


def inforegistro(request):
    message = request.session.get("message", "")
    request.session["message"] = ""

    return render(request, 'TestApp/inforegistro.html', {'inf_registro' : get_current_event().registro, 'message' : message })


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
def ponenciasAdmin(request):
    evento = get_current_event()
    ponencias_list = evento.presentacionregistro_set.all()
    return render(request, 'TestApp/AdminFront/estadoAdmin.html', {'ponencias_list' : ponencias_list})

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
    presentacion = PresentacionRegistro(presentacion_titulo=request.POST.get("pres_tit"),
                                        resp_email=request.POST.get("pres_email"),
                                        modalidad=request.POST.get("mod"),
                                        estatus="Sin revisar",
                                        evento=Evento.objects.filter(active=True).get())

    presentacion.save()

    responsable = Author(nombre=request.POST.get("resp_nom"),
                         apellido_pat=request.POST.get("resp_pat"),
                         apellido_mat=request.POST.get("resp_mat"),
                         institucion=request.POST.get("resp_inst"),
                         departamento=request.POST.get("resp_dep"),
                         grado=request.POST.get("resp_grado"),
                         presentacion=presentacion)

    responsable.save()
    
    presentacion.resp = responsable

    cant_auth=int(request.POST.get("cant_auth"))
    if cant_auth > 0:
        for x in range(1,cant_auth+1):
            autor = Author( nombre=request.POST.get("a" + str(x) + "_nom"),
                            apellido_pat=request.POST.get("a" + str(x) + "_pat"),
                            apellido_mat=request.POST.get("a" + str(x) + "_mat"),
                            institucion=request.POST.get("a" + str(x) + "_inst"),
                            departamento=request.POST.get("a" + str(x) + "_dep"),
                            grado=request.POST.get("a" + str(x) + "_grado"),
                            presentacion=presentacion)
            autor.save()

    presentacion.save()

    request.session["message"] = "Registro de ponencia exitoso!"
    return HttpResponseRedirect(reverse('TestApp:Registro')) 

###########################
# Controladores

@login_required
def insert_iter(request):
    year = request.POST.get("year")

    if Evento.objects.filter(year = year).count() > 0:
        request.session["success_message"] = "No se pueden registrar dos eventos de un mismo año!"
        return HttpResponseRedirect(reverse('TestApp:Edicion_Iteraciones'))

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

    return redirect(reverse('TestApp:Edicion_Iteraciones')) 

def report(request):
    nombre = request.POST.get('nombre_completo')
    modalidad = request.POST.get('modalidad')
    titulo = request.POST.get('title_pres')
    
    current_event = get_current_event()
    fecha = current_event.fecha;
    lugar = current_event.lugar;
        

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
    pdf.multi_cell(w = 0, h = height, txt= nombre, border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, '', size)
    pdf.multi_cell(w = 0, h = height, txt= 'Por haber asistido y presentado su ' + modalidad + ' con título', border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, 'I', size)
    pdf.multi_cell(w = 0, h = height, txt= titulo, border = 0 ,align ='c')
    pos = pdf.get_y() + 5
    
    pdf.set_xy(10,pos)
    pdf.set_font(font, '', size)
    pdf.multi_cell(w = 0, h = height, txt= 'el día ' + str(fecha) + ' en ' + lugar + '.', border = 0 ,align ='c')
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

    return redirect(reverse('TestApp:Edicion_Iteraciones')) 

    
def activate_event(request):
    year = request.POST.get("activar")

    active_events = Evento.objects.filter(active = True)

    for i in active_events:
        i.active = False
        i.save()

    to_activate = Evento.objects.get(year = year)
    to_activate.active = True
    to_activate.save()

    return redirect(reverse('TestApp:Edicion_Iteraciones'))


# return true if email_address is valid, false if is not valid
def valid_email_address(email_address):
   return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address) != None


def send_email(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    to_email = request.POST.get('to_email')
    from_email = request.POST.get('from_email')
    fpass = request.POST.get('pass')
        
    current_event = get_current_event();
        
    #correo = current_event.correo_comunicacion;
    #cpass = current_event.correo_contrasena;
    
    if not valid_email_address(from_email) :
        return render(request, "TestApp/AdminFront/correos.html", { "message" : "El correo registrado por el administrador no es válido" })
    
    if not valid_email_address(to_email) :
        return render(request, "TestApp/AdminFront/correos.html", { "message" : "El correo destinatario no es válido" })    
    
    try:
        send_mail(subject, message, from_email, [to_email], False, from_email, fpass,)
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

