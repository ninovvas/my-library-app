from datetime import date

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from MyLibrary.accounts.forms import UserModel
from MyLibrary.accounts.models import Profile
from MyLibrary.main.models import Author, Publisher, Book


class CreateBookViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'test@user.bg',
        'password': '63576Hgdh_kd'
    }

    VALID_BOOK = {
        'title': 'Book One',
        'description': 'Description Book',
        'isbn10': '1234567890',
        'isbn13': '1234567890234',
        'image': 'http://test/image.png',
        'page_count': 38,
        'language': 'de',
    }

    VALID_AUTHOR_DATA = {
        'name': 'Toshko Spasev',
        'email': 'author@test.bg',
        'picture': 'https://test.png',
    }

    VALID_PUBLISHER = {
        'publisher_name': 'Publisher One'
    }

    def __create_valid_user_and_book(self):
        #user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        # profile = Profile.objects.create(
        #     **self.VALID_PROFILE_DATA,
        #     user=user,
        # )
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)

        permission = Permission.objects.get(
            codename='add_book',
        )
        user.user_permissions.add(permission)

        author = Author.objects.create(
            **self.VALID_AUTHOR_DATA,
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

        book.authors.add(author)

        return (user, author, publisher, book)

    def test_author_create__when_create_author__expect_new_author(self):
        user, author, publisher, book = self.__create_valid_user_and_book()


        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('add book'))
        self.assertEqual(response.status_code, 200)
        #Author
        self.assertEqual(self.VALID_AUTHOR_DATA['name'], author.name)
        self.assertEqual(self.VALID_AUTHOR_DATA['email'], author.email)
        self.assertEqual(self.VALID_AUTHOR_DATA['picture'], author.picture)
        #Book
        self.assertEqual(self.VALID_BOOK['title'], book.title)
        self.assertEqual(self.VALID_BOOK['image'], book.image)
        self.assertEqual(self.VALID_BOOK['isbn10'], book.isbn10)
        self.assertEqual(self.VALID_BOOK['isbn13'], book.isbn13)
        self.assertEqual(self.VALID_BOOK['description'], book.description)
        self.assertEqual(self.VALID_BOOK['page_count'], book.page_count)
        self.assertEqual(self.VALID_BOOK['language'], book.language)
        #Publisher
        self.assertEqual(self.VALID_PUBLISHER['publisher_name'], publisher.publisher_name)
        #Test Template
        self.assertTemplateUsed('main/dashboard.html')
