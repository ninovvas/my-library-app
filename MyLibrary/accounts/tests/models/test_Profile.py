from django.core.exceptions import ValidationError
from django.test import TestCase

from MyLibrary.accounts.models import Profile, AppUser


class ProfileTests(TestCase):

    def setUp(self) -> None:
        self.TEST_USER_DEFAULT = {
            'email': 'test@user.bg',
            'password': '63576Hgdh_kd'
        }
        self.user = AppUser(**self.TEST_USER_DEFAULT)
        #self.user.save()
        self.user_pk = self.user.pk
        self.VALID_PROFILE_DATA = {
            'first_name': 'Sascha',
            'last_name': 'Dokov',
            'picture': 'http://test/image.png',
            'date_of_birth': '1990-12-24',
            'description': 'Test description',
            'gender': 1,
            'user':  self.user,
        }

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        self.user.save()
        profile.save()
        self.assertIsNotNone(profile.pk)


    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = 'Sascha9'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            description=self.VALID_PROFILE_DATA['description'],
            gender=self.VALID_PROFILE_DATA['gender'],
            user=self.user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            self.user.save()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_under_line__expect_to_fail(self):
        first_name = 'Sascha_'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            description=self.VALID_PROFILE_DATA['description'],
            gender=self.VALID_PROFILE_DATA['gender'],
            user=self.user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            self.user.save()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'Sascha Kamaran'
        profile = Profile(
            first_name=first_name,
            last_name=self.VALID_PROFILE_DATA['last_name'],
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            description=self.VALID_PROFILE_DATA['description'],
            gender=self.VALID_PROFILE_DATA['gender'],
            user=self.user,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            self.user.save()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)

        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, profile.full_name)

