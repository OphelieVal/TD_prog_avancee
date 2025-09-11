from django.contrib import admin
from .models import *

class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    list_display =  ["refProd", "intituleProd", "prixUnitaireProd", "dateFabProd", "categorie", "status"]
    list_editable = ["intituleProd", "prixUnitaireProd", "dateFabProd"]

class ProduitInline(admin.TabularInline):
    model = Produit
    extra = 1 # nombre de lignes vides par défaut

class CategorieAdmin(admin.ModelAdmin):
    model = Categorie
    inlines = [ProduitInline]

admin.site.register(Produit, ProduitAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Statut)
admin.site.register(Rayon)
admin.site.register(Contenir)