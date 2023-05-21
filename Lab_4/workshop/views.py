from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse(f"{request.GET.keys()}: {[i[0] for i in request.GET.values()]}")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Terminalo.</h1>")
