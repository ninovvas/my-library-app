from django.urls import path

from MyLibrary.main.views.author_view import CreateAuthorView, AuthorsView, DetailsAuthorView, EditAuthorView, \
    DeleteAuthorView
from MyLibrary.main.views.book_view import CreateBookView, SearchBookView, EditBookView, DetailsBookView, DeleteBookView
from MyLibrary.main.views.publisher_view import PublishersView, CreatePublisherView, DetailsPublisherView, \
    EditPublisherView
from MyLibrary.main.views.main_view import IndexView, DashboardView, UserSearchBookView

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', CreateBookView.as_view(), name='add book'),
    path('book/search/', SearchBookView.as_view(), name='search book'),
    path('book/search_user/', UserSearchBookView.as_view(), name='user search book'),
    path('book/edit/<int:pk>/', EditBookView.as_view(), name="edit book"),
    path('book/details/<int:pk>/', DetailsBookView.as_view(), name="details book"),
    path('book/delete/<int:pk>/', DeleteBookView.as_view(), name="delete book"),

    path('authors/', AuthorsView.as_view(), name="authors view"),
    path('author/create/', CreateAuthorView.as_view(), name="create author"),
    path('author/details/<int:pk>', DetailsAuthorView.as_view(), name="details author"),
    path('author/edit/<int:pk>', EditAuthorView.as_view(), name="edit author"),
    path('author/delete/<int:pk>', DeleteAuthorView.as_view(), name="delete author"),

    path('publisher/', PublishersView.as_view(), name="publishers view"),
    path('publisher/create', CreatePublisherView.as_view(), name="add publisher"),
    path('publisher/details/<int:pk>', DetailsPublisherView.as_view(), name="details publisher"),
    path('publisher/edit/<int:pk>', EditPublisherView.as_view(), name="edit publisher"),


]