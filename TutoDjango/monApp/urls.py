from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path('home/<param>',views.home ,name='home'),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path("produits/", views.ListProduits, name="list_produits")
]