import unittest

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from ..views import main_page


class MainPageTest(TestCase):
    def test_uses_home_page_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home_page.html')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
