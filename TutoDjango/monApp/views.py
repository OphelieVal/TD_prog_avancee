from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from .forms import *
from .models import Produit, Categorie, Statut, Rayon
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.mail import send_mail

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


class EmailSentView(TemplateView):
    template_name = "email_sent.html"
    def get_context_data(self, **kwargs):
        context = super(EmailSentView, self).get_context_data(**kwargs)
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)


def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via TutoDjango Contact form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@monApp.com'],
            )
            return redirect('email_sent')
    else:
        form = ContactUsForm()
    print('La méthode de requête est : ', request.method)
    print('Les données POST sont : ', request.POST)
    return render(request, "page_home.html",{'titreh1':titreh1, 'form':form})


class AboutView(TemplateView):
    template_name = "page_home.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    def post(self, request, **kwargs):
        return render(request, self.template_name)


# Produits CRUD

class ProduitDetailView(DetailView):
    model = Produit
    template_name = "detail_produit.html"
    context_object_name = "prdt"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context

class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "create_produit.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "update_produit.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "delete_produit.html"
    success_url = reverse_lazy('lst_prdts')   

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

 
# Catégorie CRUD
   
class CatDetailView(DetailView):
    model = Categorie
    template_name = "detail_categorie.html"
    context_object_name = "cat"

    def get_context_data(self, **kwargs):
        context = super(CatDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context
    
class CategorieCreateView(CreateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "create_categorie.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_categorie', cat.idCat)

def ListCategories(request):
    cats = Categorie.objects.all()
    return render(request, 'list_categories.html', {'cats': cats})


# Statut CRUD

class StatutDetailView(DetailView):
    model = Statut
    template_name = "detail_status.html"
    context_object_name = "stat"

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context

class StatutCreateView(CreateView):
    model = Statut
    form_class=StatutForm
    template_name = "create_statut.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_statut', stat.idStatus)

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'list_statuts.html', {'stats': stats})


# Rayon CRUD

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "detail_rayon.html"
    context_object_name = "ray"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context
    
class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "create_rayon.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_rayon', stat.idRayon)

def ListRayons(request):
    rays = Rayon.objects.all()
    return render(request, 'list_rayons.html', {'rays': rays})


# Authentification

class ConnectView(LoginView):
    template_name = 'page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'page_home.html', {'param': lgn, 'message': "Vous êtes connecté"})
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