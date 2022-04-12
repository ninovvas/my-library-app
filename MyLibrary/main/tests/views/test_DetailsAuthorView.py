from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

class DetailsAuthorView(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Sascha',
        'last_name': 'Dokov',
        'picture': 'http://test/image.png',
        'date_of_birth': date(1994, 9, 23),
        'description': 'Test description',
        'gender': '1',
    }

    VALID_AUTHOR_DATA = {
        'name': 'Toshko Spasev',
        'email': 'author@test.bg',
        'picture': 'https://test.png',
    }
