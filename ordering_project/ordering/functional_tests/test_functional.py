import string
import time
import random

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import unittest

from django.test import TestCase, SimpleTestCase
from django.shortcuts import get_object_or_404
from django.urls import reverse

from users.models import User


class NewVisitorTest(SimpleTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

        self.base_url = 'http://127.0.0.1:8000'
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.users_url = reverse('users:list')
        self.profile_url_no_id = '/users/profile/'

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_register_login_and_check_self_profile(self):
        # Open homepage
        self.browser.get(self.base_url)

        # Check title and body text
        self.assertIn('Ordering app', self.browser.title)
        body_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertIn('Main Page', body_text)

        # Press register
        reg_button = self.browser.find_element(by=By.XPATH, value=f'//a[@href="{self.register_url}"]')
        self.assertEqual(reg_button.text, 'Register')
        reg_button.send_keys(Keys.ENTER)
        time.sleep(1)

        # Has to redirect to register page
        self.assertEqual(self.browser.current_url, self.base_url + self.register_url)

        # Enter data and submit
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        username_input = self.browser.find_element(by=By.ID, value='id_username')
        password1_input = self.browser.find_element(by=By.ID, value='id_password1')
        password2_input = self.browser.find_element(by=By.ID, value='id_password2')

        rnd_username = self.get_random_string(8)
        email_input.send_keys(f'{rnd_username}@gmail.com')
        username_input.send_keys(rnd_username)
        password1_input.send_keys('test4321')
        password2_input.send_keys('test4321')

        submit_input = self.browser.find_element(by=By.XPATH, value='//input[@type="submit"]')
        submit_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # # If successful, redirected to login page
        self.assertEqual(self.browser.current_url, self.base_url + self.login_url)

        # # Login
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        password_input = self.browser.find_element(by=By.ID, value='id_password')

        email_input.send_keys(f'{rnd_username}@gmail.com')
        password_input.send_keys('test4321')

        submit_input = self.browser.find_element(by=By.XPATH, value='//input[@type="submit"]')
        submit_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # # If successful, redirected to home page
        self.assertEqual(self.browser.current_url, self.base_url + '/')

        # Press Profile button
        profile_button = lambda: self.browser.find_element(by=By.XPATH, value='//a[contains(text(), "Profile")]')
        profile_button().send_keys(Keys.ENTER)
        time.sleep(1)

        # # Redirects to Profile info page
        self.assertIn(self.profile_url_no_id, self.browser.current_url)
        username_text = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[1]')
        email_text = self.browser.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[2]')

        self.assertEquals(username_text.text, f'username: {rnd_username}')
        self.assertEquals(email_text.text, f'email: {rnd_username}@gmail.com')

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
