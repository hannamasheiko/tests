from django.test import TestCase
from ..models import Test
from django.utils.module_loading import import_module

import_module('user', package='quiz')
from user.models import CustomUser


class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create(first_name='Big', last_name='Bob')
        Test.objects.create(author=user, title='First', test_text='This is for me')

    def test_title_label(self):
        test=Test.objects.get(id=1)
        field_label = test._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    def test_title_max_length(self):
        test=Test.objects.get(id=1)
        max_length = test._meta.get_field('title').max_length
        self.assertEquals(max_length,200)