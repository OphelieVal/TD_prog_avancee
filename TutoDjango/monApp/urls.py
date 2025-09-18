from django.urls import path
from . import views
from django.views.generic import *

urlpatterns = [
    #path("home/", views.home, name="home"),
    path("home", views.HomeView.as_view(), name="home"),
    path('home/<param>',views.HomeParamView.as_view() ,name='home_param'),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("about", views.AboutView.as_view(), name="about"),
    path("produits/",views.ProduitListView.as_view(), name="list_produits"),
    path("produit/<pk>/",views.ProduitDetailView.as_view()),
    path("categories/", views.ListCategories, name="list_categories"),
    path("statuts/", views.ListStatuts, name="list_statuts"),
    path("rayons/", views.ListRayons, name="list_rayons")
]