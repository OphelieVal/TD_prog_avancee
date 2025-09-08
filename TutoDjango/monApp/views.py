from django.shortcuts import render
from django.http import HttpResponse
from .models import Produit, Categorie, Statut

def home(request, param=""):
    return HttpResponse("<h1> Bonjour " + param + "</h1>")

def contact(request):
    return HttpResponse("<h1>Contact us</h1><p>Coming soon</p>")

def about(request):
    return HttpResponse("<h1>About us</h1><p>No description</p>")

def ListProduits(request):
    prdts = Produit.objects.all()
    res = """ 
    <h2>Liste des produits</h2>
    <ul> 
    """
    for prdt in prdts :
        res += f"<li> {prdt.intituleProd} </li>\n"
    res += """
    </ul>
    """
    return HttpResponse(res)

def ListCategories(request):
    cats = Categorie.objects.all()
    res = """
    <h2>Liste des catégories</h2>
    <ul>
    """
    for cat in cats:
        res += f"<li>{cat.nomCat}</li>\n"  
    res += """
    </ul>
    """
    return HttpResponse(res)

def ListStatuts(request):
    stats = Statut.objects.all()
    res = """
    <h2>Liste des statuts</h2>
    <ul>
    """
    for stat in stats:
        res += f"<li>{stat.libelle}</li>\n"
    res += """
    </ul>
    """
    return HttpResponse(res)