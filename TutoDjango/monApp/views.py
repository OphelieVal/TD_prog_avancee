from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Produit, Categorie, Statut

def home(request, param=""):
    if request.GET and request.GET["test"]:
        raise Http404
    string = request.GET['name']
    return HttpResponse("Bonjour %s!" % string)

def contact(request):
    return HttpResponse("<h1>Contact us</h1><p>Coming soon</p>")

def about(request):
    return HttpResponse("<h1>About us</h1><p>No description</p>")

def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'list_produits.html', {'premier_produit': prdts[0]})

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