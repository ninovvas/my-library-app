from django import forms
from django.forms import ModelForm

from MyLibrary.main.models import Book, Author

class SearchBookForm(forms.Form):
    isbn = forms.CharField(max_length=255)

    class Meta:
        fields = ('isbn',)
        labels = {
            'isbn': 'ISBN',
    }


class CreateBookForm(ModelForm):
    authors = forms.CharField(
        label='Authors',
    )
    publisher = forms.CharField(
        label='Publisher',
    )

    class Meta:

        model = Book
        fields = ('title','authors','description','isbn10','isbn13','publisher','page_count','language',)
        labels = {
            'title': 'Title',
            'description': 'Description',
            'isbn10': 'ISBN-10',
            'isbn13': 'ISBN-13',
            'Pages': 'page_count',
            'language': 'Language',

    }


class AuthorsBookForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name',)
        labels = {
            'name': 'Author Name',
        }

