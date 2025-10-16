from datetime import datetime
from django.test import TestCase
from monApp.forms import ProduitForm

class ProduitFormTest(TestCase):
    def test_form_valid_data(self):
        form = ProduitForm(data = {'intituleProd': 'ProduitPourTest'})
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide

    def test_form_valid_data_too_long(self):
        form = ProduitForm(data = {'intituleProd': 'ProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTestProduitPourTest', 'prixUnitaireProd': 12345678910111213})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('intituleProd', form.errors) # Le champ 'intituleProd' doit contenir une erreur
        self.assertIn('prixUnitaireProd', form.errors)
        self.assertEqual(form.errors['intituleProd'], ['Assurez-vous que cette valeur comporte au plus 200 caractères (actuellement 210).'])
        self.assertEqual(form.errors['prixUnitaireProd'], ['Assurez-vous que cette valeur comporte au plus 10 chiffres (actuellement 17).'])

    def test_form_valid_data_missed(self):
        form = ProduitForm(data = {'intituleProd': ''})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('intituleProd', form.errors) # Le champ 'intituleProd' doit contenir une erreur
        self.assertEqual(form.errors['intituleProd'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = ProduitForm(data = {'intituleProd': 'ProduitPourTest', 'prixUnitaireProd': 12.22, 'dateFabProd' : datetime.now() })
        self.assertTrue(form.is_valid())
        prod = form.save()
        self.assertEqual(prod.intituleProd, 'ProduitPourTest')
        self.assertEqual(prod.refProd, 1)
