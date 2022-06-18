import time
import re

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTestCase


# Tests to add:
# 1. Register with already existing username/email
# 2. Register with different password1 and password2


class NewVisitorTests(FunctionalTestCase):
    def test_can_register__login__check_profile__find_self_on_users_page__logout__delete(self):
        self.browser.get(self.live_server_url)

        self._test_can_register(self.random_user_data)
        self._test_can_login(self.random_user_data)
        self.wait_for_redirect(self.home_url)

        self._test_correct_profile_info(self.random_user_data)
        self._test_self_username_on_users_page(self.random_user_data)

        self._test_can_logout()

        self._test_can_login(self.random_user_data)
        self.wait_for_redirect(self.home_url)

        self.get_and_press_a_link('Users', self.users_url)
        self.wait_for_redirect(self.users_url)

        self.get_and_press_a_link(self.random_user_data['username'])
        self.wait_for_redirect(self.profile_url_no_id, approx=True)

        self._test_can_delete_self_profile(self.random_user_data)

    # For now without existence check for test1 and test2 users
    def test_can_access_other_profile_info_pops_error(self):
        # User test1 logins
        self.browser.get(self.live_server_url)
        self._test_can_login(self.test1_user_data)
        self.wait_for_redirect(self.home_url)

        # User test1 tries to get profile info for test2 -> pops an error
        users_button = self.get_and_press_a_link('Users', self.users_url)
        self.wait_for_redirect(self.users_url)

        user2_link = self.get_and_press_a_link(self.test2_user_data['username'])
        error_alert = self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='.error'))
        self.assertIn('Cant access another profiles info', error_alert.text)


    def _test_can_register(self, user_data):
        # Press register
        reg_link = self.get_and_press_a_link('Register', self.register_url)
        self.wait_for_redirect(self.register_url)

        # Enter register data
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        username_input = self.browser.find_element(by=By.ID, value='id_username')
        password1_input = self.browser.find_element(by=By.ID, value='id_password1')
        password2_input = self.browser.find_element(by=By.ID, value='id_password2')

        email_input.send_keys(user_data['email'])
        username_input.send_keys(user_data['username'])
        password1_input.send_keys(user_data['password'])
        password2_input.send_keys(user_data['password'])

        # Submit data -> redirects to login page
        submit = self.get_and_press_submit_input()
        self.wait_for_redirect(self.login_url)

    def _test_can_login(self, user_data):
        # Press Login button
        if self.login_url not in self.browser.current_url:
            login_button = self.get_and_press_a_link('Login', self.login_url)
            self.wait_for_redirect(self.login_url)

        # Enter register data and submit
        email_input = self.browser.find_element(by=By.ID, value='id_email')
        password_input = self.browser.find_element(by=By.ID, value='id_password')

        email_input.send_keys(user_data['email'])
        password_input.send_keys(user_data['password'])

        # Submit data -> redirects to home page
        submit_input = self.get_and_press_submit_input()

    def _test_correct_profile_info(self, user_data):
        # Press Profile button
        profile_button = self.get_and_press_a_link('Profile', self.profile_url_no_id)
        self.wait_for_redirect(self.profile_url_no_id, approx=True)

        id_text = self.browser.find_element(by=By.ID, value='user_id').text
        username_text = self.browser.find_element(by=By.ID, value='username').text
        email_text = self.browser.find_element(by=By.ID, value='email').text

        id_from_url = self.find_profile_id_from_url(self.browser.current_url)

        self.assertEquals(id_text, f'id: {id_from_url}')
        self.assertEquals(username_text, f'username: {user_data["username"]}')
        self.assertEquals(email_text, f'email: {user_data["email"]}')

    def _test_self_username_on_users_page(self, user_data):
        # Press Users button
        users_button = self.get_and_press_a_link('Users', self.users_url)
        self.wait_for_redirect(self.users_url)

        username_link = self.get_username_link_on_users_page(self.random_user_data['username'])
        self.assertEqual(username_link.text, user_data['username'])

    def _test_can_logout(self):
        # Press Logout button
        logout_button = self.get_and_press_a_link('Logout', self.logout_url)
        self.wait_for_redirect(self.login_url)

    def _test_can_delete_self_profile(self, user_data):
        user_id = self.find_profile_id_from_url(self.browser.current_url)
        delete_button = self.get_and_press_a_link('Delete', f'{self.profile_url_no_id}{user_id}/delete')
        self.wait_for_redirect(self.login_url, approx=True)

        self._test_can_login(user_data)

        error_alert = self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='.error'))
        self.assertIn('Invalid username or password', error_alert.text)

    def find_profile_id_from_url(self, url):
        return re.findall(fr'{self.profile_url_no_id}([0-9]*)', url)[0]

    def get_username_link_on_users_page(self, username):
        username_link = self.browser.find_element(
            by=By.XPATH,
            value=f'//a[contains(text(), "{username}")]'
        )
        return username_link

    def get_and_press_submit_input(self):
        submit_input = self.browser.find_element(by=By.XPATH, value='//input[@type="submit"]')
        submit_input.send_keys(Keys.ENTER)
        return submit_input

    def get_a_link_by_text(self, link_text, url_in_href=None):
        link = self.browser.find_element(by=By.XPATH, value=f'//a[contains(text(), "{link_text}")]')
        if url_in_href:
            link_href = link.get_property('href')
            self.assertIn(url_in_href, link_href), f'WebElement link`s href is {link} != {url_in_href}'
        return link

    def get_and_press_a_link(self, link_text, url_in_href=None):
        link = self.get_a_link_by_text(link_text, url_in_href)
        link.send_keys(Keys.ENTER)
        return link
