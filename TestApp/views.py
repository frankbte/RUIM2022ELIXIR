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

    if request.session.get("showing_year", "no_event") == "no_event" or get_current_event(request).year == get_current_event(request,True).year:
        past_events = Evento.objects.filter(year__lt = current_event.year).order_by('-year')


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
def iterAdmin(request):
    eventos = Evento.objects.all()
    
    message = request.session.get("success_message", "")
    request.session["success_message"] = ""
        
    current_editing_event = get_editing_event()

    return render(request, 'TestApp/AdminFront/edicionesFront.html', 
                    {'iteracion' : current_editing_event, 'iteracion_list' : eventos, 'message' : message,
                'evento' : current_editing_event})

@login_required
def disable_registro(request):
    active_event = get_current_event(request, True)

    active_event.register_available = not active_event.register_available
    active_event.save()

    return HttpResponseRedirect(reverse('TestApp:Edicion_Iteraciones'))
            

@login_required
def create_iter(request):
    return render(request, 'TestApp/AdminFront/creacionIteracion.html',
            {'evento' : get_editing_event()})


@login_required
def informe(request):
    evento_actual = get_editing_event()
    
    pres_list = evento_actual.presentacionregistro_set.all()
    pres_total = pres_list.count()
    
    pres_acept = pres_list.filter(estatus='Aceptado').count()
    pres_rechaz = pres_list.filter(estatus='Rechazado').count()
    
    ponencias = pres_list.filter(modalidad='Ponencia')
    ponen_acept = ponencias.filter(estatus='Aceptado').count()
    ponen_rechaz = ponencias.filter(estatus='Aceptado').count()
    ponen_total = ponencias.count()
    
    carteles = pres_list.filter(modalidad='Cartel')
    cart_acept = carteles.filter(estatus='Aceptado').count()
    cart_rechaz = carteles.filter(estatus='Rechazado').count()
    cart_total = carteles.count()
    

    est = 0
    lic = 0
    ing = 0
    mtr = 0
    doc = 0
    for pres in pres_list:
        autores = Author.objects.filter(presentacion = pres)
        for autor in autores:
            match autor.grado:
                case 'Estudiante':
                    est = est+1
                case 'Licenciatura':
                    lic = lic+1
                case 'Ingeniería':
                    ing = ing+1
                case 'Maestria':
                    mtr = mtr+1
                case 'Doctorado':
                    doc = doc+1

    return render(request, 'TestApp/AdminFront/informe.html',
            {
                'evento' : evento_actual,
                'pres_total' : pres_total,
                'ponen_total' : ponen_total,
                'cart_total' : cart_total,
                'pres_acept' : pres_acept,
                'pres_rechaz' : pres_rechaz,
                'ponen_acept' : ponen_acept,
                'ponen_rechaz' : ponen_rechaz,
                'cart_acept' : cart_acept,
                'cart_rechaz' : cart_rechaz,
                'est' : est,
                'lic' : lic,
                'ing' : ing,
                'mtr' : mtr,
                'doc' : doc
            })
                

# Inicio
@login_required
def inicioAdmin(request):
    event = get_editing_event()
    form = InicioPageForm(initial={'title_descripcion': event.inicio.title_descripcion,
                                   'text_descripcion': event.inicio.text_descripcion})
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/inicioAdmin.html', 
            {'form': form, 'evento' : event, 'message' : message})

@login_required
def processInicio(request):
    evento=get_editing_event()
    
    evento.inicio = InicioPage(title_descripcion = request.POST.get('title_descripcion'),
                               text_descripcion = request.POST.get('text_descripcion'),
                               title_news = request.POST.get('title_news'),
                               text_news = request.POST.get('text_news'),
                               cartel = request.FILES.get('cartel'))
    if evento.inicio.cartel:
        try: 
            FileExtensionValidator(allowed_extensions = ['jpg', 'jpeg', 'png'])(evento.inicio.cartel)
        except ValidationError:
            request.session['message'] = "Extensión incorrecta para archivos. Intenta de nuevo."
            return(HttpResponseRedirect(reverse('TestApp:Edición Inicio')))
        evento.inicio.cartel.name = str(evento.year) + 'banner.png'
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Página de inicio actualizada para el evento " + str(evento.year)
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Inicio')) )


# Poster
@login_required
def posterAdmin(request):
    editing_event = get_editing_event()

    form = PosterPageForm()
    message = request.session.get("message", "")
    request.session["message"] = ""
    return render(request, 'TestApp/AdminFront/posterAdmin.html', 
            {'form': form,
                'message' : message, 'evento' : editing_event})
    
@login_required
def processPoster(request):
    evento=get_editing_event()
    evento.poster = PosterPage(poster_img = request.FILES.get('poster_img'),
                                  poster_pdf = request.FILES.get('poster_pdf'))

    try: 
        FileExtensionValidator(allowed_extensions = ['jpg', 'jpeg', 'png'])(evento.poster.poster_img)
        FileExtensionValidator(allowed_extensions = ['pdf'])(evento.poster.poster_pdf)
    except ValidationError:
        request.session['message'] = "Extensión incorrecta para archivos. Intenta de nuevo."
        return(HttpResponseRedirect(reverse('TestApp:Edición Poster')))

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

    try: 
        FileExtensionValidator(allowed_extensions = ['jpg', 'jpeg', 'png'])(evento.programa.programa_img)
        FileExtensionValidator(allowed_extensions = ['pdf'])(evento.programa.programa_pdf)
    except ValidationError:
        request.session['message'] = "Extensión incorrecta para archivos. Intenta de nuevo."
        return(HttpResponseRedirect(reverse('TestApp:Edición Programa')))
        

    evento.programa.programa_img.name = str(evento.year) + 'programa.jpg'
    evento.programa.programa_pdf.name = str(evento.year) + 'programa.pdf'
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Programa actualizado."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Programa')))


#Ubicacion
@login_required
def ubicacionAdmin(request):
    editing_ev = get_editing_event()

    form = UbicacionPageForm(initial = {'title' : editing_ev.ubicacion.title,
        'text' : editing_ev.ubicacion.text, 'url_maps_embed' : editing_ev.ubicacion.url_maps_embed,
        'url_maps' : editing_ev.ubicacion.url_maps})
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

    event = get_editing_event()

    form = ContactoPageForm(initial = {'title' : event.contacto.title,
        'text' : event.contacto.text, 'contacto' : event.contacto.contacto})
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
    
    event = get_editing_event()
    form = RegistroPageForm(initial = {'title_participacion_ponente' : event.registro.title_participacion_ponente,
        'text_participacion_ponente' : event.registro.text_participacion_ponente,
        'title_formato_resumen' : event.registro.title_formato_resumen,
        'text_formato_resumen' : event.registro.text_formato_resumen,
        'title_constancias_participacion' : event.registro.title_constancias_participacion,
        'text_constancias_participacion' : event.registro.text_constancias_participacion,
        'title_participacion_asistente' : event.registro.title_participacion_asistente,
        'text_participacion_asistente' : event.registro.text_participacion_asistente})

    return render(request, 'TestApp/AdminFront/registroAdmin.html', 
            {'form': form, 'evento' : get_editing_event(), 'message' : message})

@login_required
def processRegistro(request):
    evento=get_editing_event()
    evento.registro = RegistroPage(title_participacion_ponente= request.POST.get('title_participacion_ponente'), 
                                 text_participacion_ponente = request.POST.get('text_participacion_ponente'),
                                 title_formato_resumen = request.POST.get('title_formato_resumen'),
                                 text_formato_resumen = request.POST.get('text_formato_resumen'),
                                 title_constancias_participacion = request.POST.get('title_constancias_participacion'),
                                 text_constancias_participacion = request.POST.get('text_constancias_participacion'),
                                 title_participacion_asistente = request.POST.get('title_participacion_asistente'),
                                 text_participacion_asistente = request.POST.get('text_participacion_asistente'),
                                 formato_resumen_pdf = request.POST.get('formato_resumen_pdf'))

    try: 
        FileExtensionValidator(allowed_extensions = ['pdf'])(evento.registro.formato_resumen_pdf)
    except ValidationError:
        request.session['message'] = "Extensión incorrecta para archivos. Intenta de nuevo."
        return(HttpResponseRedirect(reverse('TestApp:Edición Registro')))
    
    try:
        evento.save_all()
        evento.save() 
        request.session['message'] = "Página de Registro actualizada."
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return(HttpResponseRedirect(reverse('TestApp:Edición Registro')) )


# Estado
@login_required
def estadoAdmin(request):
    evento = get_editing_event()
    message = request.session.get("message", "")
    request.session["message"] = ""
    ponencias_list = evento.presentacionregistro_set.all()
    return render(request, 'TestApp/AdminFront/estadoAdmin.html', 
            {'ponencias_list' : ponencias_list, 
             'evento' : evento,
             'message' : message})
    
@login_required
def processEstado(request):
    pk = request.POST.get('pk')
    presentacion = PresentacionRegistro.objects.get(pk = pk)
    presentacion.estatus = request.POST.get('estatus')
    
    try:
        presentacion.save() 
        request.session['message'] = "Cambio guardado." + presentacion.presentacion_titulo
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return redirect(reverse('TestApp:Estado')) 

@login_required
def getResumen(request):
    pk = request.POST.get('pk')
    presentacion = PresentacionRegistro.objects.get(pk = pk)
    resumen = presentacion.resumen.path
    
    return FileResponse(open(resumen, 'rb'), as_attachment=True, content_type= 'application/pdf')


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
            
    return render(request, 'TestApp/AdminFront/constancias.html', {'authors_list' : authors_list, 
                                                                   'message' : message,
                                                                   'ponencias_list' : ponencias_list, 
                                                                   'evento' : evento})

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
    
    
    return redirect(reverse('TestApp:Constancias')) 


# Correos
@login_required
def correos(request):
    evento = get_editing_event()
    message = request.session.get("message", "")
    request.session["message"] = ""
    ponencias_list = evento.presentacionregistro_set.all()
    return render(request, 'TestApp/AdminFront/correos.html', {'evento' : evento,
                                                               'message' : message,
                                                               'ponencias_list' : ponencias_list,})
    
@login_required
def processCorreo(request):
    user= request.POST.get('user')
    password = request.POST.get('password')
    evento = get_editing_event()
    evento.correo_comunicacion = user
    evento.correo_contrasena = password
    
    try:
        evento.save() 
        request.session['message'] = "Correo cambiado." 
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    return(HttpResponseRedirect(reverse('TestApp:Correo')) )

@login_required
def send_email(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    to_email = request.POST.get('to_email')
    
    current_event = get_editing_event();
    from_email = current_event.correo_comunicacion;
    fpass = current_event.correo_contrasena;
    
    if not valid_email_address(from_email) :
        request.session['message'] = request.session['message']+"Ocurrió un error: El correo emisor no es válido"
        return(HttpResponseRedirect(reverse('TestApp:Correo')) )
    
    if not valid_email_address(to_email) :
        request.session['message'] = request.session['message']+"Ocurrió un error: El correo destinatario no es válido"
        return(HttpResponseRedirect(reverse('TestApp:Correo')) )

    # Manually open the connection
    try:
        connection = EmailBackend(host='smtp-mail.outlook.com',port=587, username=from_email, password=fpass, use_tls=True) 
        connection.open()
    except Exception as error:
        request.session['message'] = "Ocurrió un error: " + format(error)
    
    email = EmailMessage(subject, message, from_email, [to_email], connection=connection)

    try:
        email.send(fail_silently=False)
        request.session['message'] = "Correo enviado a " + to_email 
        
    except Exception as error:
        request.session['message'] = "Ocurrió un error: " + format(error)
        
    
    connection.close()
    
    return redirect(reverse('TestApp:Correo')) 


############################
############################

def AddPresentation(request):
    presentacion_titulo = request.POST.get("pres_tit")
    evento = get_current_event(request)
    to_email = ''
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
        to_email = presentacion.resp_email
        
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
    request.session["message"] = "Registro de presentación exitoso!\n\n"
    
    """    
    ## Envio de correo
    subject = 'Reunion Universitaria de investigación de materiales ' + str(evento.year)
    message = '¡Muchas gracias por tu participación!\n Hemos recibido tu solicitud, pronto te llegará un correo de parte del comité organizador.'
    
    from_email = evento.correo_comunicacion;
    fpass = evento.correo_contrasena;
    
    if not valid_email_address(from_email) :
        request.session['message'] = request.session['message'] + "Ocurrió un error inesperado, correo de confirmación no enviado debido a configuración de correos"
        return HttpResponseRedirect(reverse('TestApp:Registro'))
    
    if not valid_email_address(to_email) :
        request.session['message'] = request.session['message'] + "El correo registrado es inválido, correo de confirmación no enviado"
        return HttpResponseRedirect(reverse('TestApp:Registro'))

    # Manually open the connection
    try:
        connection = EmailBackend(host='smtp-mail.outlook.com',port=587, username=from_email, password=fpass, use_tls=True) 
        connection.open()
        
        email = EmailMessage(subject, message, from_email, [to_email], connection=connection)
        email.send(fail_silently=False)
        request.session['message'] = request.session['message'] + "Correo de confirmación enviado a " + to_email 

        connection.close()
    except Exception as error:
        request.session['message'] = request.session['message'] + "Ocurrió un error inesperado, correo de confirmación no enviado"
        connection.close()
    """
    
    return HttpResponseRedirect(reverse('TestApp:Registro')) 

###########################
# Controladores

@login_required
def insert_iter(request):
    year = request.POST.get("year")

    if Evento.objects.filter(year = year).count() > 0:
        request.session["success_message"] = "No se pueden registrar dos eventos de un mismo año!"
        return HttpResponseRedirect(reverse('TestApp:Edicion_Iteraciones'))

    correo = request.POST.get("correo")
    correo_contrasena = request.POST.get("correo_contrasena")
    fecha = request.POST.get("date")
    lugar = request.POST.get("place")
    plantilla_constancias = request.FILES.get("plantilla_constancias")

    new_event = Evento()
    new_event.active = False
    new_event.editing = False
    new_event.register_available = False
    new_event.year = year
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
        validator = FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])

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
    pk = request.POST.get('pk')
    presentacion = PresentacionRegistro.objects.get(pk = pk)
    
    authors = Author.objects.filter(presentacion = presentacion)
    
    modalidad = presentacion.modalidad
    titulo = presentacion.presentacion_titulo
    
    current_event = presentacion.evento
    fecha = current_event.fecha;
    lugar = current_event.lugar;
        
    request.session['message'] = "Constancias creadas: \n\n"
    
    for author in authors:
        nombre = author.nombre+ ' ' + author.apellido_pat+ ' ' + author.apellido_mat

        font = 'times'
        size = 20
        height = 12
        
        pdf = FPDF('L', 'mm', 'letter')
        pdf.set_text_color(0,0,0)
        
        pdf.add_page()
        pdf.image(current_event.plantilla_constancias_img, x=0, y=0, w=280, h=216)
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
        
        pdfname = 'constancia' + str(current_event.year) + '-' + nombre.replace(' ','_') + '-' + titulo.replace(' ','_') + '.pdf'
        dest = 'TestApp/static/TestApp/archivos/constancias/'
        pdf.output(dest + pdfname, 'F')
        
        try:
            pdf.output(dest + pdfname, 'F')
            request.session['message'] = request.session['message'] + " " + pdfname + "\n"
        except Exception as error:
            request.session['message'] = "Ocurrió un error inesperado: " + format(error)
    
    
    return redirect(reverse('TestApp:Constancias'))
    #return FileResponse(open(dest + pdfname, 'rb'), as_attachment=True, content_type= 'application/pdf')

@login_required
def remove_iteration(request):

    pk = request.POST.get("pk") #Desde el view, la seleccion de evento es a trav\'es del a\~no.
    print(request.POST.get("del"))

    if request.POST.get("del") == 'true':
        
        try:
            
            event = Evento.objects.get(pk = pk)
            print(event.year)
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
            request.session["success_message"] = "Ha ocurrido un error!"

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
        i.register_available = False
        i.save()

    to_activate = Evento.objects.get(year = year)
    to_activate.active = True
    to_activate.save()

    request.session['showing_year'] = "no_event"

    return redirect(reverse('TestApp:Edicion_Iteraciones'))


# return true if email_address is valid, false if is not valid
def valid_email_address(email_address):
   return re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address) != None


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

