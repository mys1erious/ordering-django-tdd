import string
import time
import random

from django.test import TestCase
from django.urls import reverse
from dotenv import load_dotenv

from selenium import webdriver
from selenium.common import WebDriverException

from config.utils import get_env_variable

load_dotenv()


MAX_WAIT = 10
WAIT_PAUSE = 0.5


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTestCase(TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

        self.admin_data = {
            'email': get_env_variable('SUPERUSER_EMAIL'),
            'username': get_env_variable('SUPERUSER_USERNAME'),
            'password': get_env_variable('SUPERUSER_PASSWORD'),
        }
        self.test1_user_data = {
            'email': 'test1@gmail.com',
            'username': 'test1',
            'password': 'test4321',
        }
        self.test2_user_data = {
            'email': 'test2@gmail.com',
            'username': 'test2',
            'password': 'test4321',
        }
        self.random_user_data = self.generate_random_test_user_data()

        self.live_server_url = get_env_variable('BASE_URL')
        self.home_url = self.live_server_url + '/'
        self.register_url = self.live_server_url + reverse('users:register')
        self.login_url = self.live_server_url + reverse('users:login')
        self.users_url = self.live_server_url + reverse('users:list')
        self.profile_url_no_id = self.live_server_url + '/users/profile/'
        self.logout_url = self.live_server_url + reverse('users:logout')

        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_redirect(self, new_url, approx=False):
        if approx:
            self.assertIn(new_url, self.browser.current_url)
        else:
            self.assertEqual(self.browser.current_url, new_url)

    def generate_random_test_user_data(self):
        rnd_username = self.get_random_string(8)
        user_data = {
            'email': f'{rnd_username}@gmail.com',
            'username': rnd_username,
            'password': 'test4321',
        }
        return user_data

    def get_random_string(self, length):
        # Choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
