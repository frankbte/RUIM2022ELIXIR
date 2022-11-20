from django.shortcuts import render, redirect
from django.db import models
from TestApp.forms import AuthorForm, EventoForm, InicioPageForm, ContactoPageForm, UbicacionPageForm, PresentacionForm, RegistroPageForm, PosterPageForm, ProgramaPageForm
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro, UbicacionPage, PosterPage, RegistroPage, ProgramaPage, Author, DEFAULT_EVENT
from TestApp import urls
from django.http import FileResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail, EmailMessage 
from django.core.mail.backends.smtp import EmailBackend
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotModified, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import re
import copy
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
    
from fpdf import FPDF

def home(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/home.html', 
            {'home' : current_event.inicio, 'evento' : current_event})

def programa(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/programa.html', 
            {'programa' : current_event.programa, 'evento' : current_event})

def poster(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/poster.html', 
            {'poster' : current_event.poster, 'evento' : current_event})

def ubicacion(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/ubicacion.html', 
            {'ubicacion' : current_event.ubicacion, 'evento' : current_event})


def contacto(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/contacto.html', 
            {'contacto' : current_event.contacto, 'evento' : current_event})


def ponencias(request):
    current_event = get_current_event(request)
    return render(request, 'TestApp/ponencias.html', 
            {'registro': current_event.registro, 'evento' : current_event})

def ediciones(request):
    current_event = get_current_event(request)

    past_events = (Evento.objects.filter(active = True) | Evento.objects.filter(year__lt = current_event.year)).order_by('-year') 

    if request.session.get("showing_year", "no_event") == "no_event":
        past_events = Evento.objects.filter(year__lt = current_event.year).order_by('year')


    return render(request, 'TestApp/ediciones.html', 
            {'edicion' : current_event.edicion, 'evento' : current_event,
                'past_events' : past_events})


def inforegistro(request):
    message = request.session.get("message", "")
    request.session["message"] = ""

    current_event = get_current_event(request)
    return render(request, 'TestApp/inforegistro.html', {'inf_registro' : current_event.registro, 'message' : message , 'evento' : current_event})


# Vistas de administrador

def administrador_redirect_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("TestApp:Edicion_Iteraciones"))

    return HttpResponseRedirect(reverse("TestApp:login"))

@login_required
def baseFront(request):
    return render(request, 'TestApp/AdminFront/baseAdmin.html')


@login_required
def correos(request):
    evento = get_editing_event()
    return render(request, 'TestApp/AdminFront/correos.html', {'evento' : evento})


@login_required
def iterAdmin(request):
    eventos = Evento.objects.all()
    
    message = request.session.get("success_message", "")
    request.session["success_message"] = ""
        
    current_editing_event = get_editing_event()

    return render(request, 'TestApp/AdminFront/edicionesFront.html', 
                    {'iteracion' : current_editing_event, 'iteracion_list' : eventos, 'message' : message,
                'evento' : current_editing_event})
            

@login_required
def create_iter(request):
    return render(request, 'TestApp/AdminFront/creacionIteracion.html',
            {'evento' : get_editing_event()})


@login_required
def informe(request):
    return render(request, 'TestApp/AdminFront/informe.html',
            {'evento' : get_editing_event()})

# Inicio
@login_required
def inicioAdmin(request):
    form = InicioPageForm()
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/inicioAdmin.html', 
            {'form': form, 'evento' : get_editing_event(), 'message' : message})

@login_required
def processInicio(request):
    evento=get_editing_event()
    
    evento.inicio = InicioPage(title_descripcion = request.POST.get('title_descripcion'),
                               text_descripcion = request.POST.get('text_descripcion'))
    
    try:
        evento.inicio.save_all()
        evento.inicio.save() 
        request.session['message'] = "Página de inicio actualizada."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Inicio')) )


# Poster
@login_required
def posterAdmin(request):
    form = PosterPageForm()
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/posterAdmin.html', 
            {'form': form,
             'message' : message})
    
@login_required
def processPoster(request):
    evento=get_editing_event()
    evento.poster = PosterPage(poster_img = request.FILES.get('poster_img'),
                                  poster_pdf = request.FILES.get('poster_pdf'))
    evento.poster.poster_img.name = str(evento.year) + 'poster.jpg'
    evento.poster.poster_pdf.name = str(evento.year) + 'poster.pdf'

    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Poster actualizado."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error) 
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Poster')) )


# Programa
@login_required
def programaAdmin(request):
    form = ProgramaPageForm()
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/programaAdmin.html', 
            {'form': form,
             'message' : message})
    
@login_required
def processPrograma(request):
    evento=get_editing_event()
    evento.programa = ProgramaPage(programa_img = request.FILES.get('programa_img'),
                                  programa_pdf = request.FILES.get('programa_pdf'))
    evento.programa.programa_img.name = str(evento.year) + 'programa.jpg'
    evento.programa.programa_pdf.name = str(evento.year) + 'programa.pdf'
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Programa actualizado."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Programa')) )


#Ubicacion
@login_required
def ubicacionAdmin(request):
    form = UbicacionPageForm()
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/ubicacionAdmin.html', 
            {'form': form,
             'message' : message})
    
@login_required
def processUbicacion(request):
    evento=get_editing_event()
    evento.ubicacion = UbicacionPage(title = request.POST.get('title'), text = request.POST.get('text'),
                                     url_maps_embed = request.POST.get('url_maps_embed'), url_maps = request.POST.get('url_maps'))
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Página de ubicación actualizada."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error) 
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Ubicacion')) )


# Contacto
@login_required
def contactoAdmin(request):
    message = request.session.get("message", "")
    request.session["message"] = ""
    form = ContactoPageForm()
    return render(request, 'TestApp/AdminFront/contactoAdmin.html', 
            {'form': form, 'evento' : get_editing_event(), 'message' : message})

@login_required
def processContacto(request):
    evento=get_editing_event()
    evento.contacto = ContactoPage(title= request.POST.get('title'), 
                                 text = request.POST.get('text'),
                                 contacto = request.POST.get('contacto'))
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Página de contacto actualizada."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Contacto')) )


# Registro
@login_required
def registroAdmin(request):
    message = request.session.get("message", "")
    request.session["message"] = ""
    form = RegistroPageForm()
    return render(request, 'TestApp/AdminFront/registroAdmin.html', 
            {'form': form, 'evento' : get_editing_event(), 'message' : message})

@login_required
def processRegistro(request):
    evento=get_editing_event()
    evento.registro = RegistroPage(title= request.POST.get('title'), 
                                 text = request.POST.get('text'),
                                 registro = request.POST.get('registro'))
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Página de Registro actualizada."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Registro')) )


# Estado
@login_required
def ponenciasAdmin(request):
    evento = get_editing_event()
    message = request.session.get("message", "")
    request.session["message"] = ""
    ponencias_list = evento.presentacionregistro_set.all()
    return render(request, 'TestApp/AdminFront/estadoAdmin.html', 
            {'ponencias_list' : ponencias_list, 
             'evento' : evento,
             'message' : message})


# Constancias
@login_required
def constancias(request):
    evento = get_editing_event()
    message = request.session.get("message", "")
    request.session["message"] = ""
    ponencias_list = evento.presentacionregistro_set.all()
    authors_list = []
    
    for ponencia in ponencias_list:
        autores = Author.objects.filter(presentacion = ponencia)
        for autor in autores:
            authors_list.append(autor)
            
    return render(request, 'TestApp/AdminFront/constancias.html', {'authors_list' : authors_list, 'message' : message})

@login_required
def processConstancia(request):
    evento=get_editing_event()
    evento.fecha =request.POST.get('date')
    evento.lugar = request.POST.get('place')
    evento.plantilla_constancias_img = request.FILES.get('plantilla')
    evento.plantilla_constancias_img.name = str(evento.year) + 'plantilla.jpg'
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Datos de constancia actualizados."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Constancias')) )

############################
############################

def AddPresentation(request):
    presentacion_titulo = request.POST.get("pres_tit")
    evento = get_current_event(request)
    try:
        presentacion = PresentacionRegistro(presentacion_titulo = request.POST.get("pres_tit"),
                                        resp_email = request.POST.get("pres_email"),
                                        modalidad = request.POST.get("mod"),
                                        resumen = request.FILES.get("resumen"),
                                        estatus = "Sin revisar",
                                        evento = evento)

        FileExtensionValidator(allowed_extensions = ['pdf'])(presentacion.resumen)
        
        presentacion.resumen.name = str(evento.year) + presentacion_titulo.replace(' ','_') + '.pdf'
        presentacion.save()
        
    except ValidationError:
        request.session["message"] = "El resumen debe tener extensión .pdf!\n Vuelve a intentarlo con un archivo válido"
        return HttpResponseRedirect(reverse('TestApp:Registro')) 


    responsable = Author(nombre = request.POST.get("resp_nom"),
                         apellido_pat = request.POST.get("resp_pat"),
                         apellido_mat = request.POST.get("resp_mat"),
                         institucion = request.POST.get("resp_inst"),
                         departamento = request.POST.get("resp_dep"),
                         grado = request.POST.get("resp_grado"),
                         presentacion = presentacion)

    responsable.save()
    
    presentacion.resp = responsable

    cant_auth=int(request.POST.get("cant_auth"))
    if cant_auth > 0:
        for x in range(1,cant_auth+1):
            autor = Author( nombre = request.POST.get("a" + str(x) + "_nom"),
                            apellido_pat = request.POST.get("a" + str(x) + "_pat"),
                            apellido_mat = request.POST.get("a" + str(x) + "_mat"),
                            institucion = request.POST.get("a" + str(x) + "_inst"),
                            departamento = request.POST.get("a" + str(x) + "_dep"),
                            grado = request.POST.get("a" + str(x) + "_grado"),
                            presentacion = presentacion)
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

    cartel = request.FILES.get("cartel")
    correo = request.POST.get("correo")
    correo_contrasena = request.POST.get("correo_contrasena")
    fecha = request.POST.get("date")
    lugar = request.POST.get("place")
    plantilla_constancias = request.FILES.get("plantilla_constancias")

    new_event = Evento()
    new_event.active = False
    new_event.editing = False
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
        validator = FileExtensionValidator(allowed_extensions=["jpg", "jpeg"])

        validator(new_event.cartel)
        validator(new_event.plantilla_constancias_img)
        new_event.save_all()
        new_event.save() 
        request.session["success_message"] = "Nuevo evento creado con información default para vistas de usuario."
    except Evento.DoesNotExist:
        request.session["success_message"] = "No se pudo crear el evento!"
    except ValidationError as err:
        request.session["success_message"] = "Los archivos que ingresaste no tienen la extensión correcta!!!\nPor favor intenta de nuevo con otros archivos"

    return redirect(reverse('TestApp:Edicion_Iteraciones')) 



@login_required
def report(request):
    
    nombre = request.POST.get('nombre_completo')
    modalidad = request.POST.get('modalidad')
    titulo = request.POST.get('title_pres')
    
    current_event = get_editing_event()
    fecha = current_event.fecha;
    lugar = current_event.lugar;

    font = 'times'
    size = 20
    height = 12
    
    pdf = FPDF('L', 'mm', 'letter')
    pdf.set_text_color(0,0,0)
    
    pdf.add_page()
    pdf.image('TestApp/static/TestApp/archivos/admin/' + current_event.plantilla_constancias_img, x=0, y=0, w=280, h=216)
    pdf.image('TestApp/static/TestApp/archivos/admin/Escudo_Unison.png', x=15, y=7, w=35, h=40)
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
    
    pdfname = 'constancia' + str(current_event.year) + '-' + nombre.replace(' ','_') + '-' + titulo.replace(' ','_') + '.pdf'
    dest = 'TestApp/static/TestApp/archivos/constancias/'
    pdf.output(dest + pdfname, 'F')
    
    return FileResponse(open(dest + pdfname, 'rb'), as_attachment=True, content_type= 'application/pdf')

@login_required
def remove_iteration(request):
    event_year = request.POST.get("eliminar") #Desde el view, la seleccion de evento es a trav\'es del a\~no.

    try:
        event = Evento.objects.get(year = event_year)
        event.inicio.delete()
        event.programa.delete()
        event.poster.delete()
        event.ubicacion.delete()
        event.contacto.delete()
        event.registro.delete()
        event.edicion.delete()
        event.delete()

        request.session["success_message"] = "Evento eliminado!"

    except Evento.DoesNotExist:
        request.session["seccess_message"] = "Ha ocurrido un error!"

    return redirect(reverse('TestApp:Edicion_Iteraciones')) 

@login_required
def change_editing_event(request):
    year = request.POST.get("editar")

    currently_editing = get_editing_event()
    currently_editing.editing = False
    currently_editing.save()

    new_editing = Evento.objects.get(year = year)
    new_editing.editing = True
    new_editing.save()

    request.session["success_message"] = "Ahora puedes editar la información de la edición " + str(year) + " en las demás pestañas" 
    return HttpResponseRedirect(reverse('TestApp:Edicion_Iteraciones'))

def change_viewing_event(request, year):
    request.session['showing_year'] = year

    return HttpResponseRedirect(reverse('TestApp:Home'))

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

@login_required
def send_email(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    to_email = request.POST.get('to_email') # A list or tuple of recipient addresses.
    from_email = request.POST.get('from_email')
    fpass = request.POST.get('pass')
    
    if from_email=='':
        current_event = get_current_event(request, True);
        from_email = current_event.correo_comunicacion;
        fpass = current_event.correo_contrasena;
    
    if not valid_email_address(from_email) :
        return  HttpResponseBadRequest('El correo emisor no es válido')
    
    if not valid_email_address(to_email) :
        return HttpResponseBadRequest('El correo destinatario no es válido')

    # Manually open the connection
    connection = EmailBackend(host='smtp-mail.outlook.com',port=587, username=from_email, password=fpass, use_tls=True) 
    connection.open()
    
    email = EmailMessage(subject, message, from_email, [to_email], connection=connection)

    try:
        email.send(fail_silently=False)
    except BadHeaderError:
        return  HttpResponseForbidden('Invalid header found.')
    
    connection.close()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def get_current_event(request, admin = False):
    showing_year = request.session.get("showing_year", "no_event")

    if showing_year != "no_event" and (not admin):
        showing_year = int(showing_year)
        showing_event = Evento.objects.filter(year = showing_year)

        if showing_event.count() == 1:
            return showing_event[0]


    eventos = Evento.objects.all()

    if eventos.count() > 0:
        eventos = eventos.filter(active = True)
        if eventos.count() > 0:
            return eventos[0]

        eventos = Evento.objects.all()
        eventos[0].active = True
        eventos[0].save()
        return eventos[0]

    return copy.deepcopy(DEFAULT_EVENT)

def get_editing_event():
    editing_events = Evento.objects.filter(editing = True)

    if editing_events.count() == 0:
        if Evento.objects.all().count() == 0:
            q = copy.deepcopy(DEFAULT_EVENT)
            q.year = "Sin eventos!"
            return q
        new_editing = Evento.objects.all()[0]
        new_editing.editing = True
        new_editing.save()
        return new_editing

    if editing_events.count() > 1:
        for i in range(1, editing_events.count() - 1):
            editing_events[i].editing = False

    return editing_events[0]

