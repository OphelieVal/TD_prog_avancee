from django.test import TestCase
from monApp.forms import RayonForm

class RayonFormTest(TestCase):
    def test_form_valid_data(self):
        form = RayonForm(data = {'nomRayon': 'RayonPourTest'})
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide

    def test_form_valid_data_too_long(self):
        form = RayonForm(data = {'nomRayon': 'RayonPourTestRayonPourTestRayonPourTestRayonPourTestRayonPourTestRayonPourTest'})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('nomRayon', form.errors) # Le champ 'nomRayon' doit contenir une erreur
        self.assertEqual(form.errors['nomRayon'], ['Assurez-vous que cette valeur comporte au plus 100 caractères (actuellement 102).'])

    def test_form_valid_data_missed(self):
        form = RayonForm(data = {'nomRayon': ''})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('nomRayon', form.errors) # Le champ 'nomRayon' doit contenir une erreur
        self.assertEqual(form.errors['nomRayon'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = RayonForm(data = {'nomRayon': 'RayonPourTest'})
        self.assertTrue(form.is_valid())
        ray = form.save()
        self.assertEqual(ray.nomRayon, 'RayonPourTest')
        self.assertEqual(ray.idRayon, 1)