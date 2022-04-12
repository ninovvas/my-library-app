import os
import urllib
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from cloudinary.compat import urllib2
from django import forms
from django.core.files import File
from django.forms import ModelForm

from MyLibrary.common.helper import DisabledFieldsFormMixin
from MyLibrary.main.models import Book, Author, Publisher


class SearchBookForm(forms.Form):
    input_search = forms.CharField(max_length=255)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        fields = ('input_search',)
        labels = {
            'input_search': 'ISBN or Title',
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
            #if book.user.has_perm('main.create_book')
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
            'image': 'URL Image',
            'page_count': 'Pages',
            'language': 'Language',

    }


class AuthorsBookForm(ModelForm):
    class Meta:
        model = Author
        fields = ('name',)
        labels = {
            'name': 'Author Name',
        }


class EditBookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        #queryset = super().get_queryset()
        queryset = Book.objects.get(user=self.instance.user, authors__book__authors=self.object.id)
        return queryset

    class Meta:
        model = Book
        exclude = ['user']


class DetailsBookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Book
        exclude = ['user']


class DeleteBookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Book
        exclude = ['user']



##################
#Authors
##################

class DetailsAuthorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Author
        exclude = ['user']

class CreateAuthorForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):

        if commit:
            try:
                new_author = Author.objects.get(
                    name=self.cleaned_data['name'],
                    user=self.user
                )
            except Author.DoesNotExist:
                new_author = Author(
                    name=self.cleaned_data['name'],
                    email=self.cleaned_data['email'],
                    user_id=self.user.id
                )
            new_author.save()

        return new_author

    class Meta:
        model = Author
        fields = ('name','email', 'picture')
        labels = {
            'name': 'Name',
            'email': 'Email',
            'picture': 'URL Image',
        }

class EditAuthorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = Author.objects.get(user=self.instance.user, user__author=self.object.id)
        return queryset

    class Meta:
        model = Author
        fields = ['name', 'email', 'picture']
        labels = {
            'name': 'Name',
            'email': 'Email',
            'picture': 'URL Image',
        }







