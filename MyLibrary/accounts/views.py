from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeView

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from MyLibrary.accounts.forms import CreateProfileForm, EditProfileForm
from MyLibrary.accounts.models import Profile
from MyLibrary.common.view_mixins import RedirectToDashboard
from MyLibrary.main.models import Book


class UserRegisterView(RedirectToDashboard,CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        # user => self.object
        # request => self.request
        login(self.request, self.object)
        return result

class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    #success_url = reverse_lazy('dashboard')
    success_url_dashboard = reverse_lazy('dashboard')
    success_url_search_book = reverse_lazy('search book')

    def get_success_url(self):
        book = Book.objects.all()
        if book:
            return self.success_url_dashboard
        else:
            return self.success_url_search_book

        # if self.success_url:
        #     return self.success_url
        # return super().get_success_url()


class ProfileLogoutView(LogoutView):
    template_name = 'accounts/logout_page.html'
    success_url = reverse_lazy('logout user')

class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = list(Book.objects.filter(user_id=self.object.user_id))
        books_read = list(Book.objects.filter(user_id=self.object.user_id, read__exact=True))

        total_books_count = len(books)
        total_read_books = len(books_read)

        context.update({
            'total_books_count': total_books_count,
            'total_read_books': total_read_books,
            'is_owner': self.object.user_id == self.request.user.id,
            'books': books,
        })

        return context

class ChangeProfilePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'


class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('details profile', kwargs={'pk': self.object.user_id})

class UserResetPasswordView(PasswordResetView):
    pass