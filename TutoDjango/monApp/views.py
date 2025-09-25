from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Produit, Categorie, Statut, Rayon
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

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
    
class CatDetailView(DetailView):
    model = Categorie
    template_name = "detail_categorie.html"
    context_object_name = "cat"

    def get_context_data(self, **kwargs):
        context = super(CatDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context
    
def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'list_categories.html', {'cats': cats})

class StatutDetailView(DetailView):
    model = Statut
    template_name = "detail_status.html"
    context_object_name = "stat"

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'list_statuts.html', {'stats': stats})

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "detail_rayon.html"
    context_object_name = "ray"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context

def ListRayons(request):
    rays = Rayon.objects.all()
    return render(request, 'list_rayons.html', {'rays': rays})


class ConnectView(LoginView):
    template_name = 'page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'page_register.html')
        
class RegisterView(TemplateView):
    template_name = 'page_register.html'
    def post(self, request, **kwargs):
        user = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(user, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'page_login.html', {'message': "Vous pouvez maintenant vous connecter"})
        else:
            return render(request, 'page_register.html')
        
class DisconnectView(TemplateView):
    template_name = 'page_home.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name, {'message': "Vous êtes déconnecté"})