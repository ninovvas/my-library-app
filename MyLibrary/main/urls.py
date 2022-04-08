from django.urls import path

from MyLibrary.main.views.book_view import CreateBookView, SearchBookView, EditBookView, DetailsBookView, DeleteBookView
from MyLibrary.main.views.category_view import CategoryView
from MyLibrary.main.views.main_view import IndexView, DashboardView, UserSearchBookView

urlpatterns = [

    path('', IndexView.as_view(), name='index'), #as_view(template_name="index.htm"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', CreateBookView.as_view(), name='add book'),
    path('book/search/', SearchBookView.as_view(), name='search book'),
    path('book/search_user/', UserSearchBookView.as_view(), name='user search book'),
    path('book/edit/<int:pk>/', EditBookView.as_view(), name="edit book"),
    path('book/details/<int:pk>/', DetailsBookView.as_view(), name="details book"),
    path('book/delete/<int:pk>/', DeleteBookView.as_view(), name="delete book"),

    path('admin/category/', CategoryView.as_view(), name='category view'),

]