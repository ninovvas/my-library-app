from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.forms import UserModel
from MyLibrary.main.models import Author

class AuthorsViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }

    VALID_AUTHOR_DATA = {
        'name': 'Toshko Spasev',
        'email': 'author@test.bg',
        'picture': 'https://test.png',
    }

    def test_authors__when_data_valid__expect_2_authors_and_statuscode_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )

        author_one_data = {
            'name': 'Toshko Spasev',
            'email': 'author@test.com',
            'picture': 'https://test_uthor.png',
        }

        author1 = Author.objects.create(
            **author_one_data,
            user=user,
        )


        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('authors view'))
        self.assertEqual(response.status_code, 200)

        authors = response.context['object_list']

        self.assertEqual(2, len(authors))
        self.assertTemplateUsed('main/authors.html')

    def test_authors__when_correct_data__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/authors.html')

    def test_authors_when_no_permissions__expect_error_302(self):
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

        response = self.client.get(reverse('authors view'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard')


