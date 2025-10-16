from django.test import TestCase
from monApp.forms import ContenirForm, ProduitForm, RayonForm

class ContenirFormTest(TestCase):
    def test_form_valid_data(self):
        produit = ProduitForm(data = {'intituleProd': 'ProduitPourTest'})
        form = ContenirForm(data = {'produit': produit, 'Qte': 10})
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide