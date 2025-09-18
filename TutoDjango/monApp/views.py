from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Produit, Categorie, Statut, Rayon
from django.views.generic import *

#def home(request, param=""):
#    if request.GET and request.GET["test"]:
#        raise Http404
#    string = request.GET['name']
#    return HttpResponse("Bonjour %s!" % string)

class HomeView(TemplateView):
    template_name = "page_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    

class HomeParamView(TemplateView):
    template_name = "page_home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomeParamView, self).get_context_data(**kwargs)
        param = self.kwargs.get('param', '')
        context['titreh1'] = f"Hello DJANGO, param = {param}"
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)


#def contact(request):
#    return render(request, 'contact.html')

class ContactView(TemplateView):
    template_name = "page_home.html"
    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['titreh1'] = "Don't hesitate to contact us !"
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)

#def about(request):
#    return render(request, 'about.html')

class AboutView(TemplateView):
    template_name = "page_home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)

#def ListProduits(request):
#    prdts = Produit.objects.all()
#    return render(request, 'list_produits.html', {'prdts': prdts})

class ProduitDetailView(DetailView):
    model = Produit
    template_name = "detail_produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context

class ProduitListView(ListView):
    model = Produit
    template_name = "list_produits.html"
    context_object_name = "prdts"
    def get_queryset(self ) :
        return Produit.objects.order_by("prixUnitaireProd")
    
    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context  
    
def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'list_categories.html', {'cats': cats})

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'list_statuts.html', {'stats': stats})

def ListRayons(request):
    rays = Rayon.objects.all()
    return render(request, 'list_rayons.html', {'rays': rays})