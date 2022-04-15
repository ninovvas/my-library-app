from django.contrib.auth.models import Permission
from django.urls import reverse
from django.test import TestCase

from MyLibrary.accounts.forms import UserModel
from MyLibrary.main.models import Publisher


class CreatePublisherViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }

    VALID_PUBLISHER_DATA = {
        'publisher_name': 'dPunkt',
        'address': 'Solonska 56',
        'email': 'publisher@mail.de',
        'city': 'Heidelberg',
        'state_province':'Baden Wuertenberg',
        'country': 'Germany',
        'website': 'www.dpunkt.de',
        'icon': 'http://depunkt/icon.png'
    }

    def test_publisher_create__when_create_publisher__expect_new_publisher_codestatus_200(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_publisher',
        )
        user.user_permissions.add(permission)

        publisher = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )

        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('add publisher'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.VALID_PUBLISHER_DATA['publisher_name'], publisher.publisher_name)
        self.assertEqual(self.VALID_PUBLISHER_DATA['email'], publisher.email)
        self.assertEqual(self.VALID_PUBLISHER_DATA['city'], publisher.city)
        self.assertEqual(self.VALID_PUBLISHER_DATA['address'], publisher.address)
        self.assertEqual(self.VALID_PUBLISHER_DATA['state_province'], publisher.state_province)
        self.assertEqual(self.VALID_PUBLISHER_DATA['country'], publisher.country)
        self.assertEqual(self.VALID_PUBLISHER_DATA['website'], publisher.website)
        self.assertEqual(self.VALID_PUBLISHER_DATA['icon'], publisher.icon)
        self.assertTemplateUsed('main/publisher.html')

    def test_publisher_create__when_create_exist_publisher__expect_not_create_new_publisher_with_same_name(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_publisher',
        )
        user.user_permissions.add(permission)

        publisher = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )



        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('add publisher'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.VALID_PUBLISHER_DATA['publisher_name'], publisher.publisher_name)
        self.assertEqual(self.VALID_PUBLISHER_DATA['email'], publisher.email)
        self.assertEqual(self.VALID_PUBLISHER_DATA['city'], publisher.city)
        self.assertEqual(self.VALID_PUBLISHER_DATA['address'], publisher.address)
        self.assertEqual(self.VALID_PUBLISHER_DATA['state_province'], publisher.state_province)
        self.assertEqual(self.VALID_PUBLISHER_DATA['country'], publisher.country)
        self.assertEqual(self.VALID_PUBLISHER_DATA['website'], publisher.website)
        self.assertEqual(self.VALID_PUBLISHER_DATA['icon'], publisher.icon)
        self.assertTemplateUsed('main/publisher.html')

        publisher1 = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )

        response = self.client.post(reverse('add publisher'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.VALID_PUBLISHER_DATA['publisher_name'], publisher1.publisher_name)
        self.assertEqual(self.VALID_PUBLISHER_DATA['email'], publisher1.email)
        self.assertEqual(self.VALID_PUBLISHER_DATA['city'], publisher1.city)
        self.assertEqual(self.VALID_PUBLISHER_DATA['address'], publisher1.address)
        self.assertEqual(self.VALID_PUBLISHER_DATA['state_province'], publisher1.state_province)
        self.assertEqual(self.VALID_PUBLISHER_DATA['country'], publisher1.country)
        self.assertEqual(self.VALID_PUBLISHER_DATA['website'], publisher1.website)
        self.assertEqual(self.VALID_PUBLISHER_DATA['icon'], publisher1.icon)
        self.assertTemplateUsed('main/publisher.html')
        #
        # publishers = Publisher.objects.filter(publisher_name=publisher)
        # self.assertEqual(1, len(publishers))

    def test_publisher_when_no_permissions__expect_error_302(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='view_publisher',
        )
        user.user_permissions.add(permission)

        author = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add publisher'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('main/dashboard')

    def test_publisher_create__when_correct_data__expect_use_correct_template(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_publisher',
        )
        user.user_permissions.add(permission)

        author = Publisher.objects.create(
            **self.VALID_PUBLISHER_DATA,
            user=user,
        )
        self.assertTemplateUsed('main/publisher_create.html')


