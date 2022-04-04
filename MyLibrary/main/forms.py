import os
import urllib
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from cloudinary.compat import urllib2
from django import forms
from django.core.files import File
from django.forms import ModelForm

from MyLibrary.main.models import Book, Author, Publisher


class SearchBookForm(forms.Form):
    isbn = forms.CharField(max_length=255)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

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

    image = forms.URLField(
        label='Image URL',
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    # def clean(self, *args, **kwargs):
    #     all_data = self.cleaned_data
    #     url_image = all_data['image']
    #     if url_image:
    #         img_temp = NamedTemporaryFile(delete=True)
    #         img_temp.write(urlopen(url_image).read())
    #         img_temp.flush()
    #         all_data['image'] = File(img_temp)
    #
    #     return all_data

    def save(self, commit=True):
        #return the created object
        book = super().save(commit=False)
        book.user = self.user


        if commit:
            #authors
            l_authors = self.__manage_authors(self.cleaned_data['authors'])
            l_authors_obj = []
            for auth in l_authors:
                try:
                    author = Author.objects.get(
                        name=auth,
                    )
                except Author.DoesNotExist:
                    author = Author(
                        name=auth,
                        user=self.user,
                    )
                author.save()
                l_authors_obj.append(author)
            #publisher
            try:
                publisher = Publisher.objects.get(
                    publisher_name=self.cleaned_data['publisher'],
                )
            except Publisher.DoesNotExist:
                publisher = Publisher(
                    publisher_name=self.cleaned_data['publisher'],
                    user=self.user,
                )
            publisher.save()
            try:
                exist_book = Book.objects.get(
                    title=self.cleaned_data['title'],
                    user=self.user,
                )
            except Book.DoesNotExist:
                book.publisher_id = publisher.id
                book.save()
                for author in l_authors_obj:
                    book.authors.add(author)
        return book


    @staticmethod
    def __manage_authors(authors):
        separators = [",", ";", "/"]
        l_authors = []
        for separator in separators:
            if separator in authors:
                separated_authors = authors.split(separator)
                separated_authors = [a.strip() for a in separated_authors]
                l_authors += separated_authors
        if not l_authors:
            l_authors.append(authors)
        return l_authors

    class Meta:

        model = Book
        fields = ('title','description','isbn10','isbn13','image','page_count','language',)
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




