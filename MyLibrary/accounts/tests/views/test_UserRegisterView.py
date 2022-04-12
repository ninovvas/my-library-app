from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.forms import CreateProfileForm
from MyLibrary.accounts.models import AppUser, Profile

UserModel = get_user_model()

class UserRegisterViewTest(TestCase):

    def setUp(self) -> None:

        self.VALID_USER_CREDENTIALS = {
            'email': 'test@user.bg',
            'password': '63576Hgdh_kd'
        }


        self.VALID_PROFILE_DATA = {
            'first_name': 'Sascha',
            'last_name': 'Dokov',
            'picture': 'http://test/image.png',
            'date_of_birth': date(1994,9,23),
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

    def __get_response_for_create_profile(self, profile):
        return self.client.get(reverse('dashboard'))

    def __get_response_for_not_create_profile(self):
        return self.client.get(reverse('login user'))

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))

    def test_user_register__when_input_valid__expect_use_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_create_profile(profile)
        self.assertTemplateUsed('accounts/profile_create.html')

    def test_user_register__when_input_valid__expect_to_create_profile(self):
        _, profile = self.__create_valid_user_and_profile()
        self.assertIsNotNone(profile)
        self.assertEqual(self.VALID_PROFILE_DATA['first_name'], profile.first_name)
        self.assertEqual(self.VALID_PROFILE_DATA['last_name'], profile.last_name)
        self.assertEqual(self.VALID_PROFILE_DATA['last_name'], profile.last_name)
        self.assertEqual(self.VALID_PROFILE_DATA['picture'], profile.picture)
        self.assertEqual(self.VALID_PROFILE_DATA['date_of_birth'], profile.date_of_birth)
        self.assertEqual(self.VALID_PROFILE_DATA['description'], profile.description)
        self.assertEqual(self.VALID_PROFILE_DATA['gender'], profile.gender)

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('details profile', kwargs={
            'pk': 1,
        }))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('main/404_error.html')

