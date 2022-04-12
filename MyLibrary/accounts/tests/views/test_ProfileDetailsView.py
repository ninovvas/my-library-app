from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from MyLibrary.accounts.models import Profile
from MyLibrary.main.models import Author, Publisher, Book

UserModel = get_user_model()

class ProfileDetailsViewTest(TestCase):
    def setUp(self) -> None:

        self.VALID_USER_CREDENTIALS = {
            'email': 'test@user.bg',
            'password': '63576Hgdh_kd'
        }

        self.VALID_PROFILE_DATA = {
            'first_name': 'Sascha',
            'last_name': 'Dokov',
            'picture': 'http://test/image.png',
            'date_of_birth': date(1994, 9, 23),
            'description': 'Test description',
            'gender': '1',
        }

        self.VALID_BOOK = {
            'title': 'Book One',
            'description': 'Description Book',
            'isbn10': '1234567890',
            'isbn13': '1234567890234',
            'image': 'http://test/image.png',
            'page_count': 38,
            'language': 'de',
        }

        self.VALID_AUTHOR = {
            'name': 'Florian Bayer',
        }

        self.VALID_PUBLISHER = {
            'publisher_name': 'Publisher One'
        }

    def __create_valid_user_and_profile_and_book(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        author = Author.objects.create(
            **self.VALID_AUTHOR,
            user=user,
        )

        publisher = Publisher.objects.create(
            **self.VALID_PUBLISHER,
            user=user,
        )

        book = Book.objects.create(
            **self.VALID_BOOK,
            user=user,
            publisher_id=publisher.id,

        )
        #book.publisher_id = publisher.id
        #book.save()
        #book.publicher.set(publisher)
        #book.authors.set(author)
        book.authors.add(author)


        return (user, profile, author, publisher, book)

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile)

    def __get_response_for_profile_details(self, profile):
        return self.client.post(reverse('details profile', kwargs={'pk': profile.pk}))


    def test_profile_details__show_details__expect__correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile_details(profile)
        self.assertTemplateUsed('accounts/profile_details.html')

    def test_profile_details__when_profile_view__expect_context_details_view(self):
        #user, profile, authors, publisher, book = self.__create_valid_user_and_profile_and_book()
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        response = self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))
        self.assertEqual(response.status_code, 200)

        # Assert
        total_books_count = response.context['total_books_count']
        total_read_books = response.context['total_read_books']
        is_owner = response.context['is_owner']
        books = response.context['book']
        # Check for actual profiles
        self.assertEqual(0, total_books_count)
        self.assertEqual(0, total_read_books)
        self.assertTrue(is_owner, True)
        self.assertEqual(None, books)