# class AdminTests(TestCase):
#     def _test_admin_can_delete_user_profile(self):
#         self._test_can_register()
#
#         self.browser.get(self.live_server_url)
#
#         self._test_can_login()
#
#         self.get_and_press_correct_a_link('Users', self.users_url)
#         self.get_and_press_correct_a_link(self.user_data['username'])
#
#         user_id = self.find_profile_id_from_url(self.browser.current_url)
#
#         delete_button = self.get_and_press_correct_a_link('Delete', f'{self.profile_url_no_id}{user_id}/delete')
#
#         self._test_get_user_info_returns_404(pk=user_id)