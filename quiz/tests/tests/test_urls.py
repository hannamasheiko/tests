from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import tests_list


class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('test_list')
        self.assertEquals(resolve(url).func,  tests_list)