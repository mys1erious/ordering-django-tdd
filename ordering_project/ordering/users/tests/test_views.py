from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='test1',
            email='test1@gmail.com',
            password='test1'
        )
        self.user2 = User.objects.create_user(
            username='test2',
            email='test2@gmail.com',
            password='test2'
        )
        self.user_admin = User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin',
        )

        self.users_list_url = reverse('users:list')
        self.user_profile_url = reverse('users:profile', kwargs={'pk': self.user.pk})
        self.another_user_profile_url = reverse('users:profile', kwargs={'pk': self.user2.pk})
        self.login_page_url = reverse('users:login')
        self.register_page_url = reverse('users:register')

    def test_list(self):
        self.client.login(username='test1@gmail.com', password='test1')
        response = self.client.get(self.users_list_url)

        self.assertContains(response, 'test1')
        self.assertContains(response, 'test2')
#
#     def test_list_unauthorized_redirects_to_login_page(self):
#         response = self.client.get(self.users_list_url)
#         self.assertEqual(response.url, f'{self.login_page_url}?next={self.users_list_url}')
#
#     def test_profile_returns_status_code_200(self):
#         self.client.login(username='test1@gmail.com', password='test1')
#         response = self.client.get(self.user_profile_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_profile_of_another_user_redirects_to_users_list(self):
#         self.client.login(username='test1@gmail.com', password='test1')
#         response = self.client.get(self.another_user_profile_url)
#         self.assertEqual(response.url, self.users_list_url)
#
#     def test_profile_of_another_user_if_admin_returns_status_code_200(self):
#         self.client.login(username='admin@gmail.com', password='admin')
#         response = self.client.get(self.another_user_profile_url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_profile_unauthorized_redirects_to_login_page(self):
#         response = self.client.get(self.user_profile_url)
#         self.assertEqual(response.url, f'{self.login_page_url}?next={self.user_profile_url}')
#
#     def test_register_success(self):
#         # Finish this one
#         data = {
#             'email': 'test1@gmail.com',
#             'username': 'test1',
#             'password1': 'test4321',
#             'password2': 'test43210',
#         }
#         response = self.client.post(self.register_page_url, data)
#         print(response, response.status_code)
#         self.assertEqual(response.status_code, 302)
