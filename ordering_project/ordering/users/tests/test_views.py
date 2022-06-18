from django.test import TestCase
from django.urls import reverse

from users.models import User


class RegisterViewTests(TestCase):
    def setUp(self) -> None:
        self.test_user_data = {
            'email': 'test1@gmail.com',
            'username': 'test1',
            'password1': 'test4321',
            'password2': 'test4321'
        }
        self.register_page_url = reverse('users:register')

    def test_can_save_a_POST_request(self) -> None:
        response = self.client.post(self.register_page_url, self.test_user_data)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, self.test_user_data['username'])

    def test_redirects_after_POST(self) -> None:
        response = self.client.post(self.register_page_url, self.test_user_data)
        self.assertRedirects(response, reverse('users:login'))
