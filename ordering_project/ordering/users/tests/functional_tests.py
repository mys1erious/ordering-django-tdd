from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_register_login_and_check_self_profile(self):
        # Open homepage
        self.browser.get('http://localhost:8000')

        # Check title
        self.assertIn('Ordering app', self.browser.title)

        # Press register

        # Enter data and submit

        # If successful, redirected to login page

        # Login

        # If successful, redirected to home page

        # Press Profile button -> redirects to Profile info page


if __name__ == '__main__':
    unittest.main(warnings='ignore')
