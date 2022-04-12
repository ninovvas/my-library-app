from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.models import AppUser, Profile

UserModel = get_user_model()

class ProfileEditViewTest(TestCase):

    def setUp(self) -> None:

        self.VALID_USER_CREDENTIALS = {
            'email': 'test@user.bg',
            'password': '63576Hgdh_kd',
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
        user = UserModel.objects.create_user(**credentials)
        #permission = Permission.objects.get(codename='accounts.change.profile')
        #group = Group.objects.get(name='app_default')
        #group.user_set.add(user)
        #user.add(permission)
        return user



    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __get_response_for_edit_profile(self, profile):
        return self.client.post(reverse('details profile',  kwargs={'pk': profile.pk}))

    # def __get_response_for_profile(self, profile):
    #     return self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))

    # def __get_response_for_profile(self, profile):
    #     return self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))

    def test_profile_edit__when_input_valid__expect_use_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_edit_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    # def test_profile_edit__when_profile_no_permission__expect_go_to_deshabord(self):
    #     pass


    def test_profile_edit__all_data_correct__expect_edit_profile(self):
        _, profile = self.__create_valid_user_and_profile()
        self.CHANGE_PROFILE_DATA = {
            'first_name': 'Sascha',
            'last_name': 'Dokov',
            'picture': 'http://test/image.png',
            'date_of_birth': date(1980, 9, 23),
            'description': "Das Ist eoin Test"

        }


        #profile.objects.update(**self.CHANGE_PROFILE_DATA)
        #profile.objects.update({'date_of_birth': date(2022, 9, 23)})


        #Act
        response = self.client.post(reverse('edit profile',  kwargs={'pk': profile.pk}), **self.CHANGE_PROFILE_DATA)
        #response = self.client.post(reverse('edit profile',  kwargs={'pk': profile.pk}), EDIT_PROFILE_DATA)
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.date_of_birth,self.CHANGE_PROFILE_DATA['date_of_birth'])
