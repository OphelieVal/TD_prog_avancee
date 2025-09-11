from django.contrib import admin
from .models import *

class ProduitFilter(admin.SimpleListFilter):
    title = 'filtre produit'
    parameter_name = 'custom_status'
    
    def lookups(self, request, model_admin) :
        return (
        ('OnLine', 'En ligne'),
        ('OffLine', 'Hors ligne'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'OnLine':
            return queryset.filter(status=1)
        if self.value() == 'OffLine':
            return queryset.filter(status=0)

class ProduitAdmin(admin.ModelAdmin):
    model = Produit
    list_display =  ["refProd", "intituleProd", "prixUnitaireProd", "dateFabProd", "categorie", "status"]
    list_editable = ["intituleProd", "prixUnitaireProd", "dateFabProd"]
    radio_fields = {"status": admin.VERTICAL}
    search_fields = ('intituleProd', 'dateFabProd')
    list_filter = (ProduitFilter,)
    date_hierarchy = 'dateFabProd'
    ordering = ('-dateFabProd',)

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