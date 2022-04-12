from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from MyLibrary.accounts.views import UserLoginView, UserRegisterView, ProfileLogoutView, ProfileDetailsView, \
    ChangeProfilePasswordView, ProfileEditView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', ProfileLogoutView.as_view(), name='logout user'),
    path('edit/<int:pk>/', ProfileEditView.as_view(), name='edit profile'),
    path('details/<int:pk>/', ProfileDetailsView.as_view(), name='details profile'),
    path('edit-password/', ChangeProfilePasswordView.as_view(), name='change user password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),

]

