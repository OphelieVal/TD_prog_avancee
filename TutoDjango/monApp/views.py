from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from .forms import *
from .models import Produit, Categorie, Statut, Rayon, Contenir
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.db.models import Count, Prefetch

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

@method_decorator(login_required, name="dispatch")
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "create_produit.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)

@method_decorator(login_required, name="dispatch")    
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "update_produit.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
@method_decorator(login_required, name="dispatch")    
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "delete_produit.html"
    success_url = reverse_lazy('lst_prdts')   

class ProduitListView(ListView):
    model = Produit
    template_name = "list_produits.html"
    context_object_name = "prdts"
    def get_queryset(self):
        # Charge les catégories et les statuts en même temps
        return Produit.objects.select_related('categorie').select_related('status')
    
    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context  

 
# Catégorie CRUD
   
class CatDetailView(DetailView):
    model = Categorie
    template_name = "detail_categorie.html"
    context_object_name = "ctgr"
    
    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))

    def get_context_data(self, **kwargs):
        context = super(CatDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits_categorie.all()
        return context

@method_decorator(login_required, name="dispatch")    
class CategorieCreateView(CreateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "create_categorie.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_categorie', cat.idCat)

@method_decorator(login_required, name="dispatch")    
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "update_categorie.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_categorie', cat.idCat)

@method_decorator(login_required, name="dispatch")    
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "delete_categorie.html"
    success_url = reverse_lazy('list_categories')   

def ListCategories(request):
    ctgrs = Categorie.objects.all()
    return render(request, 'list_categories.html', {'ctgrs': ctgrs})

class CategorieListView(ListView):
    model = Categorie
    template_name = "list_categories.html"
    context_object_name = "ctgrs"
    
    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context


# Statut CRUD

class StatutDetailView(DetailView):
    model = Statut
    template_name = "detail_status.html"
    context_object_name = "stat"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produits_status'))

    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produits_status.all()
        return context

@method_decorator(login_required, name="dispatch")
class StatutCreateView(CreateView):
    model = Statut
    form_class=StatutForm
    template_name = "create_statut.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_statut', stat.idStatus)

@method_decorator(login_required, name="dispatch")    
class StatutUpdateView(UpdateView):
    model = Statut
    form_class=StatutForm
    template_name = "update_statut.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_statut', stat.idStatus)

@method_decorator(login_required, name="dispatch")    
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "delete_statut.html"
    success_url = reverse_lazy('list_statuts')   

def ListStatuts(request):
    stats = Statut.objects.all()
    return render(request, 'list_statuts.html', {'stats': stats})

class StatutListView(ListView):
    model = Statut
    template_name = "list_statuts.html"
    context_object_name = "stats"
    
    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    def get_context_data(self, **kwargs):
        context = super(StatutListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context



# Rayon CRUD

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "detail_rayon.html"
    context_object_name = "ray"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0
        
        for contenir in self.object.contenir_rayon.all():
            total_produit = contenir.produit.prixUnitaireProd * contenir.Qte
            prdts_dt.append({ 'produit': contenir.produit,
                            'qte': contenir.Qte,
                            'prix_unitaire': contenir.produit.prixUnitaireProd,
                            'total_produit': total_produit} )
            total_rayon += total_produit
            total_nb_produit += contenir.Qte
        
        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit
        return context

@method_decorator(login_required, name="dispatch")            
class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "create_rayon.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        stat = form.save()
        return redirect('dtl_rayon', stat.idRayon)

@method_decorator(login_required, name="dispatch")    
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class=RayonForm
    template_name = "update_rayon.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        ray = form.save()
        return redirect('dtl_rayon', ray.idRayon)

@method_decorator(login_required, name="dispatch")    
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "delete_rayon.html"
    success_url = reverse_lazy('list_rayons')

def ListRayons(request):
    rays = Rayon.objects.all()
    return render(request, 'list_rayons.html', {'rays': rays})

class RayonListView(ListView):
    model = Rayon
    template_name = "list_rayons.html"
    context_object_name = "ray"

    def get_queryset(self):
        # Précharge tous les "contenir" de chaque rayon,
        # et en même temps le produit de chaque contenir
        return Rayon.objects.prefetch_related(Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit")))
    
    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        ryns_dt = []
        for rayon in context['ray']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.Qte
            ryns_dt.append({'rayon': rayon,'total_stock': total})
        
        context['ryns_dt'] = ryns_dt
        return context


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