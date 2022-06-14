import string
import time
import random
import re
from dotenv import load_dotenv
from abc import ABC

from config.utils import get_env_variable

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import unittest

from django.test import TestCase
from django.urls import reverse


# Maybe make setups for Authenticated users and tests for different tabs?

load_dotenv()
SLEEP_TIME = 0.5


class NewVisitorTests(TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

        self.admin_data = {
            'email': get_env_variable('SUPERUSER_EMAIL'),
            'username': get_env_variable('SUPERUSER_USERNAME'),
            'password': get_env_variable('SUPERUSER_PASSWORD'),
        }
        self.user_data = self.generate_random_test_user_data()

        self.base_url = get_env_variable('BASE_URL')
        self.home_url = self.base_url + '/'
        self.register_url = self.base_url + reverse('users:register')
        self.login_url = self.base_url + reverse('users:login')
        self.users_url = self.base_url + reverse('users:list')
        self.profile_url_no_id = self.base_url + '/users/profile/'
        self.logout_url = self.base_url + reverse('users:logout')

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_register__login__check_profile__find_self_on_users_page__logout__delete(self):
        self.browser.get(self.base_url)

        self._test_can_register(self.user_data)
        self._test_can_login(self.user_data)

        self._test_correct_profile_info()
        self._test_self_username_on_users_page()

        self._test_can_logout()

        self._test_can_login(self.user_data)

        self.get_and_press_correct_a_link('Users', self.users_url)
        self.get_and_press_correct_a_link(self.user_data['username'])
        self._test_can_delete_self_profile()

    def _test_can_register(self, user_data):
        # Press register
        reg_button = self.get_and_press_correct_a_link('Register', self.register_url)

        # Redirect to register page
        self.assertEqual(self.browser.current_url, self.register_url)

        # Enter register data and submit
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        username_input = self.browser.find_element(by=By.ID, value='id_username')
        password1_input = self.browser.find_element(by=By.ID, value='id_password1')
        password2_input = self.browser.find_element(by=By.ID, value='id_password2')

        email_input.send_keys(user_data['email'])
        username_input.send_keys(user_data['username'])
        password1_input.send_keys(user_data['password'])
        password2_input.send_keys(user_data['password'])

        submit = self.get_and_press_submit_input()

        # # If successful, redirects to login page
        self.assertEqual(self.browser.current_url, self.login_url)

    def _test_can_login(self, user_data, for_success=True):
        # Press Login button
        login_button = self.get_and_press_correct_a_link('Login', self.login_url)

        # Redirects to Login page
        self.assertEqual(self.browser.current_url, self.login_url)

        # Enter register data and submit
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        password_input = self.browser.find_element(by=By.ID, value='id_password')

        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])

        submit_input = self.get_and_press_submit_input()

        # # If successful, redirects to home page

        if for_success:
            self.assertEqual(self.browser.current_url, self.home_url)
        else:
            self.assertEqual(self.browser.current_url, self.login_url)

    def _test_correct_profile_info(self):
        # Press Profile button
        profile_button = self.get_and_press_correct_a_link('Profile', self.profile_url_no_id)

        # # Redirects to Profile info page
        self.assertIn(self.profile_url_no_id, self.browser.current_url)

        # For now with hardcoded XPATH
        id_text = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]').text
        username_text = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]').text
        email_text = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]').text

        id_from_url = self.find_profile_id_from_url(self.browser.current_url)

        self.assertEquals(id_text, f'id: {id_from_url}')
        self.assertEquals(username_text, f'username: {self.user_data["username"]}')
        self.assertEquals(email_text, f'email: {self.user_data["email"]}')

    def _test_self_username_on_users_page(self):
        # Press Users button
        users_button = self.get_and_press_correct_a_link('Users', self.users_url)

        # Redirects to Users page
        self.assertEqual(self.browser.current_url, self.users_url)

        username_link = self.get_username_link_on_users_page()

        self.assertEqual(username_link().text, self.user_data['username'])

    def _test_can_logout(self):
        # Press Logout button
        logout_button = self.get_and_press_correct_a_link('Logout', self.logout_url)

        # Redirects to Login page
        self.assertEqual(self.browser.current_url, self.login_url)

    def _test_can_delete_self_profile(self):
        user_id = self.find_profile_id_from_url(self.browser.current_url)
        delete_button = self.get_and_press_correct_a_link('Delete', f'{self.profile_url_no_id}{user_id}/delete')
        self._test_can_login(self.user_data, for_success=False)

        error_alert = lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='.error')

        self.assertIn('Invalid username or password', error_alert().text)

    def test_correct_main_page(self):
        # Open homepage
        self.browser.get(self.base_url)

        # Check title and body text
        self.assertIn('Ordering app', self.browser.title)
        body_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertIn('Main Page', body_text)

    def find_profile_id_from_url(self, url):
        return re.findall(fr'{self.profile_url_no_id}([0-9]*)', url)[0]

    def get_username_link_on_users_page(self):
        username_link = lambda: self.browser.find_element(
            by=By.XPATH,
            value=f'//a[contains(text(), "{self.user_data["username"]}")]'
        )
        return username_link

    def get_and_press_submit_input(self):
        submit_input = self.browser.find_element(by=By.XPATH, value='//input[@type="submit"]')
        submit_input.send_keys(Keys.ENTER)
        time.sleep(SLEEP_TIME)
        return submit_input

    def get_and_press_correct_a_link(self, link_text, url_in_href=None):
        button = lambda: self.browser.find_element(by=By.XPATH, value=f'//a[contains(text(), "{link_text}")]')

        if url_in_href:
            self.assertIn(url_in_href, button().get_property('href'))

        button().send_keys(Keys.ENTER)
        time.sleep(SLEEP_TIME)

        return button

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


class AdminTests(TestCase):
    def _test_admin_can_delete_user_profile(self):
        self._test_can_register()

        self.browser.get(self.base_url)

        self._test_can_login()

        self.get_and_press_correct_a_link('Users', self.users_url)
        self.get_and_press_correct_a_link(self.user_data['username'])

        user_id = self.find_profile_id_from_url(self.browser.current_url)

        delete_button = self.get_and_press_correct_a_link('Delete', f'{self.profile_url_no_id}{user_id}/delete')

        self._test_get_user_info_returns_404(pk=user_id)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
