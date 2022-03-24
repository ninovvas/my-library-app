from django.urls import path

from MyLibrary.main.views.book_view import CreateBookView, SearchBookView
from MyLibrary.main.views.main_view import IndexView, DashboardView

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add', CreateBookView.as_view(), name='add book'),
    path('book/search', SearchBookView.as_view(), name='search book')
]