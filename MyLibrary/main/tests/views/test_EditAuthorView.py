from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.forms import UserModel
from MyLibrary.main.models import Author

class EditAuthorViewTest(TestCase):
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

    def test_edit_authors__when_data_valid__expect_valid_edit_author_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='change_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )

        edit_author = {
        'name': 'Toshko Spasev',
        'email': 'author@test.com',
        'picture': 'https://test_uthor.png',
    }

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('edit author', kwargs={'pk': author.pk}), data=edit_author)
        updated_author = Author.objects.get(pk=author.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(edit_author['name'], updated_author.name)
        #self.assertEqual(edit_author['email'], updated_author.email)
        #self.assertEqual(edit_author['picture'], updated_author.picture)
        self.assertTemplateUsed('main/author_details.html')

    def test_edit_authors__when_no_permission__expect_statuscode_302(self):
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

        response = self.client.post(reverse('edit author', kwargs={'pk': author.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard')

    def test_author_edit__when_correct_data__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='change_author',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/author_edit.html')
