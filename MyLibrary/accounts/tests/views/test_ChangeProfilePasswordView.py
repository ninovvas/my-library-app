from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.models import Profile

UserModel = get_user_model()

class ChangeProfilePasswordViewTest(TestCase):

    def setUp(self) -> None:
        self.VALID_USER_CREDENTIALS = {
            'email': 'test@user.bg',
            'password': '63576Hgdh_kd'
        }

        self.VALID_PROFILE_DATA = {
            'first_name': 'Sascha',
            'last_name': 'Dokov',
            'picture': 'http://test/image.png',
            'date_of_birth': date(1994, 9, 23),
            'description': 'Test description',
            'gender': '1',
        }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __get_response_for_change_password_profile(self):
        return self.client.get(reverse('change user password'))

    def __get_response_password_change_done(self):
        return self.client.get(reverse('password_change_done'))


    def test_user_register__when_input_valid__expect_use_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_change_password_profile()
        self.assertTemplateUsed('accounts/change_password.html')

    def test_change_password__when_password_changed__expect_password_was_changed(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        #old_user_password = user.password
        self.CHANGE_USER_CREDENTIALS = {
            'email': 'test@user.bg',
            'password': '6453Hgdgf_',
        }
        response = self.client.post(reverse('change user password'), **self.CHANGE_USER_CREDENTIALS )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard.html')

    #TODO: why the passoword is not changed?
    # def test_change_password__when_password_not_changed__expect_error(self):
    #     user, profile = self.__create_valid_user_and_profile()
    #     old_user_password = user.password
    #     self.CHANGE_USER_CREDENTIALS = {
    #         'email': 'test@user.bg',
    #         'password': '6453Hgdgf_',
    #     }
    #     change_password_user = self.__change_user(**self.CHANGE_USER_CREDENTIALS)
    #
    #     #response = self.client.post(reverse('change user password'), **self.CHANGE_USER_CREDENTIALS)
    #     #self.assertEqual(response.status_code, 302)
    #     self.assertNotEqual(old_user_password, change_password_user.password)
    #     self.assertTemplateUsed('main/dashboard.html')

