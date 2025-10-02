from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    path("home", views.HomeView.as_view(), name="home"),
    path('home/<param>',views.HomeParamView.as_view() ,name='home_param'),
    path("contact", views.ContactView, name="contact"),
    path("about", views.AboutView.as_view(), name="about"),

    # CRUD Produit
    path("produits/",views.ProduitListView.as_view(),name="lst_prdts"),
    path("produit/<pk>/",views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produit/",views.ProduitCreateView.as_view(), name="crt_prdt"),
    path("produit/<pk>/update/",views.ProduitUpdateView.as_view(), name="prdt_chng"),
    path("produit/<pk>/delete/",views.ProduitDeleteView.as_view(), name="prdt_del"),
    
    # CRUD Catégorie
    path("categories/", views.ListCategories, name="list_categories"),
    path('categorie/<int:pk>/', views.CatDetailView.as_view(), name='dtl_categorie'),
    path("categorie/", views.CategorieCreateView.as_view(), name="crt_cat"),
    
    # CRUD Statut
    path("statuts/", views.ListStatuts, name="list_statuts"),
    path('statut/<int:pk>/', views.StatutDetailView.as_view(), name='dtl_statut'),
    path("statut/", views.StatutCreateView.as_view(), name="crt_statut"),
    
    # CRUD Rayon
    path("rayons/", views.ListRayons, name="list_rayons"),
    path('rayon/<int:pk>/', views.RayonDetailView.as_view(), name='dtl_rayon'),
    path("rayon/", views.RayonCreateView.as_view(), name="crt_rayon"),
    
    # User authentication
    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path("email_sent/", views.EmailSentView.as_view(), name="email_sent"),
]