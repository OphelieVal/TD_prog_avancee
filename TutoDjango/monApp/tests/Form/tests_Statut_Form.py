from django.test import TestCase
from monApp.forms import StatutForm

class StatutFormTest(TestCase):
    def test_form_valid_data(self):
        form = StatutForm(data = {'libelleStatus': 'StatutPourTest'})
        self.assertTrue(form.is_valid()) # Le formulaire doit être valide

    def test_form_valid_data_too_long(self):
        form = StatutForm(data = {'libelleStatus': 'StatutPourTestStatutPourTestStatutPourTestStatutPourTestStatutPourTestStatutPourTest'})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('libelleStatus', form.errors) # Le champ 'libelleStatus' doit contenir une erreur
        self.assertEqual(form.errors['libelleStatus'], ['Assurez-vous que cette valeur comporte au plus 100 caractères (actuellement 102).'])

    def test_form_valid_data_missed(self):
        form = StatutForm(data = {'libelleStatus': ''})
        self.assertFalse(form.is_valid()) # Le formulaire doit être invalide
        self.assertIn('libelleStatus', form.errors) # Le champ 'libelleStatus' doit contenir une erreur
        self.assertEqual(form.errors['libelleStatus'], ['Ce champ est obligatoire.'])

    def test_form_save(self):
        form = StatutForm(data = {'libelleStatus': 'StatutPourTest'})
        self.assertTrue(form.is_valid())
        stat = form.save()
        self.assertEqual(stat.libelleStatus, 'StatutPourTest')
        self.assertEqual(stat.idStatus, 1)