from django.shortcuts import render



def home(request):
    return render(request, 'TestApp/home.html')
def programa(request):
    return render(request, 'TestApp/programa.html')
def poster(request):
    return render(request, 'TestApp/poster.html')
def ubicacion(request):
    return render(request, 'TestApp/ubicacion.html')
def contacto(request):
    return render(request, 'TestApp/contacto.html')
def ponencias(request):
    return render(request, 'TestApp/ponencias.html')
def ediciones(request):
    return render(request, 'TestApp/ediciones.html')

# Create your views here.
