from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.main.models import Author

UserModel = get_user_model()

class CreateAuthorViewTest(TestCase):

    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }


    VALID_AUTHOR_DATA = {
        'name': 'Toshko Spasev',
        'email': 'author@test.bg',
        'picture': 'https://test.png',
    }

    def test_author_create__when_create_author__expect_new_author(self):
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

        response = self.client.post(reverse('create author'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.VALID_AUTHOR_DATA['name'], author.name)
        self.assertEqual(self.VALID_AUTHOR_DATA['email'], author.email)
        self.assertEqual(self.VALID_AUTHOR_DATA['picture'], author.picture)
        self.assertTemplateUsed('main/authors.html')

    def test_author_create__when_create_the_same_author__expect_not_create_the_same_author(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        author1 = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('create author'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.VALID_AUTHOR_DATA['name'], author1.name)
        self.assertEqual(self.VALID_AUTHOR_DATA['email'], author1.email)
        self.assertEqual(self.VALID_AUTHOR_DATA['picture'], author1.picture)
        self.assertTemplateUsed('main/authors.html')

    def test_author_create__when_input_valid__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/author_create.html')







