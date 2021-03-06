from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.forms import UserModel
from MyLibrary.main.models import Author


class DetailsAuthorView(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }


    VALID_AUTHOR_DATA = {
        'name': 'Toshko Spasev',
        'email': 'author@test.bg',
        'picture': 'https://test.png',
    }

    UNVALID_AUTHOR_DATA = {
        'name': 'Betko Bonev',
        'email': 'author_petko@test.bg',
        'picture': 'https://test111.png',
    }

    def test_details_authors__when_data_valid__expect_valid_author(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('details author', kwargs={'pk': author.pk}))
        actual_author = response.context['object']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(author, actual_author)

    def test_details_authors__when_data_not_valid__expect_error(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )

        author1 = Author.objects.create(
            **self.UNVALID_AUTHOR_DATA,
            user=user,
        )

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('details author', kwargs={'pk': author.pk}))
        actual_author = response.context['object']

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(author1, actual_author)

    def test_author_details__when_correct_data__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/author_details.html')


    def test_author_details_when_no_permissions__expect_error_302(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('details author', kwargs={'pk': author.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard')

