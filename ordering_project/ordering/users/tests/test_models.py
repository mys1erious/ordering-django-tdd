from django.test import TestCase
from users.models import User


class UserModelsTests(TestCase):

    def test_create_user_no_email_throws_exception(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='test1',
                password='test_pas1'
            )

    def test_create_user_no_username_throws_exception(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='test1@gmail.com',
                password='test_pas1'
            )

    def test_create_user_no_password_throws_exception(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username='test1',
                email='test1@gmail.com',
            )
