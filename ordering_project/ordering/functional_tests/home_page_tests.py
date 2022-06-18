# def test_correct_main_page(self):
#     # Open homepage
#     self.browser.get(self.live_server_url)
#
#     # Check title and body text
#     self.assertIn('Ordering app', self.browser.title)
#     body_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
#     self.assertIn('Main Page', body_text)