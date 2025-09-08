from django.shortcuts import render
from django.http import HttpResponse
from .models import Produit

def home(request, param=""):
    return HttpResponse("<h1> Bonjour " + param + "</h1>")

def contact(request):
    return HttpResponse("<h1>Contact us</h1><p>Coming soon</p>")

def about(request):
    return HttpResponse("<h1>About us</h1><p>No description</p>")

def ListProduits(request):
    prdts = Produit.objects.all()
    res = """ 
    <ul> 
    """
    for prdt in prdts :
        res += f"<li> {prdt.intituleProd} </li>\n"
    res += """
    </ul>
    """
    return HttpResponse(res)