from django import forms
from django.forms import ModelForm

from MyLibrary.main.models import Book


class SearchBookForm(forms.Form):
    isbn = forms.CharField(max_length=13)

    class Meta:
        fields = ('isbn',)
        labels = {
            'isbn': 'ISBN',
    }


class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title',)
        labels = {
            'title': 'Title',

    }
