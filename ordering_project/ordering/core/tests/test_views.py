import unittest

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from ..views import main_page


class MainPageTest(TestCase):
    def test_root_url_resolves_to_main_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, main_page)

    def test_main_page_returns_correct_html(self):
        request = HttpRequest()
        response = main_page(request)
        html = response.content.decode('utf-8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<div>Main Page</div>', html)
        self.assertTrue(html.endswith('</html>'))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
