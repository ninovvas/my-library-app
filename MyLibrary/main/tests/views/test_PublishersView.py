from django.contrib.auth.models import Permission
from django.urls import reverse
from django.test import TestCase

from MyLibrary.accounts.forms import UserModel
from MyLibrary.main.models import Publisher

class PublishersViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }

    VALID_PUBLISHER_DATA = {
        'publisher_name': 'dPunkt',
        'address': 'Solonska 56',
        'email': 'publisher@mail.de',
        'city': 'Heidelberg',
        'state_province': 'Baden Wuertenberg',
        'country': 'Germany',
        'website': 'www.dpunkt.de',
        'icon': 'http://depunkt/icon.png'
    }

    def test_publisher__when_data_valid__expect_2_publisher_and_statuscode_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_publisher',
        )
        user.user_permissions.add(permission)

        author = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )

        publisher_one_data = {
        'publisher_name': 'Rechtek',
        'address': 'Mazart Strasse 4',
        'email': 'publisher1@mail.de',
        'city': 'München',
        'state_province': 'Byern',
        'country': 'Germany',
        'website': 'www.rechtek.de',
        'icon': 'http://Rechtek/icon.png'
    }

        author1 = Publisher.objects.create(
            **publisher_one_data,
            user=user,
        )

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('publishers view'))
        self.assertEqual(response.status_code, 200)

        publishers = response.context['object_list']

        self.assertEqual(2, len(publishers))
        self.assertTemplateUsed('main/publishers.html')

    def test_publisher__when_correct_data__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_publisher',
        )
        user.user_permissions.add(permission)

        author = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/publishers.html')

    def test_publisher_when_no_permissions__expect_error_302(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_publisher',
        )
        user.user_permissions.add(permission)

        author = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('publishers view'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard')
