from django.urls import path

from MyLibrary.rest_api.views import BookListAndCreateView, PublisherListAndCreateView, AuthorListAndCreateView, \
    PublisherDetailsAndUpdateView, AuthorDetailsAndUpdateView

urlpatterns = [
    path('books/', BookListAndCreateView.as_view(), name='api list or create book'),
    path('publishers/', PublisherListAndCreateView.as_view(), name='api list or create publisher'),
    path('publisher/<int:pk>', PublisherDetailsAndUpdateView.as_view(), name='api details or update publisher'),
    path('authors/', AuthorListAndCreateView.as_view(), name='api list or create author' ),
    path('author/<int:pk>', AuthorDetailsAndUpdateView.as_view(), name='api details or update author')
    ]