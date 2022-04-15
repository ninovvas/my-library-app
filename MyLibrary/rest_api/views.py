from django.core import exceptions
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from MyLibrary.main.models import Book, Publisher, Author
from MyLibrary.rest_api.serializers import BookListSerializer, BookFullSerializer, PublisherListSerializer, \
    PublisherFullSerializer, AuthorListSerializer, AuthorFullSerializer


#######
# Book
#######

class BookListAndCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )

    list_serializer_class = BookListSerializer
    create_serializer_class = BookFullSerializer

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.list_serializer_class

###########
# Publisher
###########

class PublisherListAndCreateView(ListCreateAPIView):
    queryset = Publisher.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )

    list_serializer_class = PublisherListSerializer
    create_serializer_class = PublisherFullSerializer

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.list_serializer_class


class PublisherDetailsAndUpdateView(RetrieveUpdateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherFullSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_object(self):
        the_object = super().get_object()
        if the_object.user != self.request.user:
            raise exceptions.PermissionDenied
        return the_object


#########
# Author
#########

class AuthorListAndCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
    )

    list_serializer_class = AuthorListSerializer
    create_serializer_class = AuthorFullSerializer

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.list_serializer_class


class AuthorDetailsAndUpdateView(RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorFullSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_object(self):
        the_object = super().get_object()
        if the_object.user != self.request.user:
            raise exceptions.PermissionDenied
        return the_object
