from models import Pages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context


@csrf_exempt
def cms_annotated(request, recurso):
    
    status = "logout"
    if not request.user.is_authenticated():
        salida = "No esta logueado"
        status = "loggin"
    else:
        if request.method == 'GET':
            try:
                pages = Pages.objects.get(name=recurso)
                salida = "pagina de: " + pages.page
            except Pages.DoesNotExist:
                salida = "Recurso no encontrado"
        elif request.method == 'PUT':
                p = Pages(name=recurso, page=request.body)
                p.save()
                salida = "Pagina guardada: " + request.body
        else:
            salida = "metodo no disponible"

    #Indicamos plantilla
    template = get_template("index.html")
    #Marcamos contexto:
    c = Context({'mensaje' : salida, 'loggin': status})
    renderizado = template.render(c)
    return HttpResponse(renderizado)
@csrf_exempt
def cms_users_put(request, recurso):

    status = "<p><a href='/admin/logout/'>Logout</a></p>"
    if not request.user.is_authenticated():
       return HttpResponse("<p>No esta logueado <a href='/admin/login/'> Para loguearse</a><p>")
    if request.method == 'GET':
        try:
            pages = Pages.objects.get(name=recurso)
            return HttpResponse("pagina de " + pages.page + status)
        except Pages.DoesNotExist:
            return HttpResponseNotFound("Recurso no encontrado" + status)
    elif request.method == 'PUT':
            p = Pages(name=recurso, page=request.body)
            p.save()
            return HttpResponse("Pagina guardada: " + request.body)
    else:
        return HttpResponseNotFound("metodo no disponible")
