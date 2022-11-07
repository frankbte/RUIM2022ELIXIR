from django.shortcuts import render, redirect
from django.db import models
from TestApp.forms import AuthorForm, EventoForm, InicioPageForm, ContactoPageForm, PresentacionForm
from TestApp.models import Evento, InicioPage, ContactoPage, PresentacionRegistro, Author
from django.http import FileResponse, HttpResponseRedirect

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
def evento(request):
    return render(request, 'TestApp/evento.html')

def login(request):
    return render(request, 'TestApp/AdminFront/login.html')

def constancias(request):
    return render(request, 'TestApp/AdminFront/constancias.html')

def iterAdmin(request, message = ""):
    eventos = Evento.objects.all()
    
    if Evento.objects.count() > 0:
        return render(request, 'TestApp/AdminFront/edicionesFront.html', {'iteracion' : eventos[0], 'iteracion_list' : eventos, 'message' : message})
    
    return render(request, 'TestApp/AdminFront/edicionesFront.html', {'message' : message})

def informe(request):
    return render(request, 'TestApp/AdminFront/informe.html')

def inicioAdmin(request):
    form = InicioPageForm()
    return render(request, 'TestApp/AdminFront/inicioAdmin.html', {'form': form})

def contactoAdmin(request):
    form = ContactoPageForm()
    return render(request, 'TestApp/AdminFront/contactoAdmin.html', {'form': form})


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

def savemail(request):  
    if request.method == "POST":  
        form = EventoForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = EventoForm()  
    return render(request,'index.html',{'form':form})  

def insert(request):
    presentacion_titulo = request.POST.get("presentacion_titulo")
    resp_email =  request.POST.get("resp_email")
    r_name = request.POST.get("resp_name")
    r_am = request.POST.get("resp_ap")
    r_ap = request.POST.get("resp_am")
    a1_name = request.POST.get("a1_name")
    a1_am = request.POST.get("a1_ap")
    a1_ap = request.POST.get("a1_am")
    a2_name = request.POST.get("a2_name")
    a2_am = request.POST.get("a2_ap")
    a2_ap = request.POST.get("a2_am")
    a3_name = request.POST.get("a3_name")
    a3_am = request.POST.get("a3_ap")
    a3_ap = request.POST.get("a3_am")
    a4_name = request.POST.get("a4_name")
    a4_am = request.POST.get("a4_ap")
    a4_ap = request.POST.get("a4_am")
    a5_name = request.POST.get("a5_name")
    a5_am = request.POST.get("a5_ap")
    a5_ap = request.POST.get("a5_am")
    a6_name = request.POST.get("a6_name")
    a6_am = request.POST.get("a6_ap")
    a6_ap = request.POST.get("a6_am")
    a7_name = request.POST.get("a7_name")
    a7_am = request.POST.get("a7_ap")
    a7_ap = request.POST.get("a7_am")
    institucion = request.POST.get("institucion")
    departamento = request.POST.get("departamento")
    modalidad = request.POST.get("modalidad")
    resumen = request.POST.get("resumen")

    current_events = Evento.objects.filter(active = 1)
    if current_events.count() == 1:
        register = PresentacionRegistro(presentacion_titulo = presentacion_titulo,
            resp = Author(nombre=r_name, apellido_mat = r_am, apellido_pat = r_ap).save(),
            #resp_email = resp_email,
            #a1 = Author(nombre=a1_name, apellido_mat = a1_am, apellido_pat = a1_ap).save(),
            #a2 = Author(nombre=a2_name, apellido_mat = a2_am, apellido_pat = a2_ap).save(),
            #a3 = Author(nombre=a3_name, apellido_mat = a3_am, apellido_pat = a3_ap).save(),
            #a4 = Author(nombre=a4_name, apellido_mat = a4_am, apellido_pat = a4_ap).save(),
            #a5 = Author(nombre=a5_name, apellido_mat = a5_am, apellido_pat = a5_ap).save(),
            #a6 = Author(nombre=a6_name, apellido_mat = a6_am, apellido_pat = a6_ap).save(),
            #a7 = Author(nombre=a7_name, apellido_mat = a7_am, apellido_pat = a7_ap).save(),
            institucion = institucion,
            departamento = departamento,
            modalidad = modalidad,
            resumen = resumen,
            estatus = False,
            evento = current_events[0])

        register.save()

        return render(request, "TestApp/ponencias.html", { "message" : "Registro exitoso!"})

    return render(request, "TestApp/ponencias.html", { "message" : "Registro no existoso :(" })

def remove_iteration(request):
    event_year = request.POST.get("Eliminar") #Desde el view, la seleccion de evento a borrar tiene que venir con ese nombre 
                                                    #y que corresponda con el nombre en la db.
    try:
        event = Evento.objects.get(year = event_year)
        event.delete()

    except Evento.DoesNotExist:
        eventos = Evento.objects.all()
        current_event = Evento.objects.get(active = 1)
        return render(request, 'TestApp/AdminFront/edicionesFront.html', {'iteracion' : current_event, 'iteracion_list' : eventos, 'message' : "Ocurrió un error!"})

    return HttpResponseRedirect("/edicionesAdmin")






