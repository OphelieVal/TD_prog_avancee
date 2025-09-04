from django.shortcuts import render
from django.http import HttpResponse

def home(request, param=""):
    return HttpResponse("<h1> Bonjour " + param + "</h1>")

def contact(request):
    return HttpResponse("<h1>Contact us</h1><p>Coming soon</p>")

def about(request):
    return HttpResponse("<h1>About us</h1><p>No description</p>")