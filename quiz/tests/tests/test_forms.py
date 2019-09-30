from django.test import TestCase
from django.test import Client
from ..forms import TestForm


class TestAddFormTest(TestCase):

    def testform_valid(self):
        form = TestForm(data={'title': "Ведьмак", 'test_text': "Some info about it"})
        self.assertTrue(form.is_valid())

    def testform_invalid(self):
        form = TestForm(data={'title': "", 'test_text': ""})
        self.assertFalse(form.is_valid())
