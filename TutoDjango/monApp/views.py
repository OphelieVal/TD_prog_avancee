from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Produit, Categorie, Statut, Rayon

def home(request, param=""):
    if request.GET and request.GET["test"]:
        raise Http404
    string = request.GET['name']
    return HttpResponse("Bonjour %s!" % string)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'list_produits.html', {'prdts': prdts})

def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'list_categories.html', {'cats': cats})

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'list_statuts.html', {'stats': stats})

def ListRayons(request):
    rays = Rayon.objects.all()
    return render(request, 'list_rayons.html', {'rays': rays})