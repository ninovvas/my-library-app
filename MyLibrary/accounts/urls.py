from django.urls import path

from MyLibrary.accounts.views import UserLoginView, UserRegisterView, UserLogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),


]