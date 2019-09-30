from django.test import TestCase, Client
from django.urls import reverse
from ..models import Test

from django.utils.module_loading import import_module

import_module('user', package='quiz')
from user.models import CustomUser


class TestsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(first_name='Big', last_name='Bob')
        Test.objects.create(author=user, title='Title', test_text='This is for me')

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('test_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('test_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'tests/tests_list.html')
