from django.contrib.auth import login
from django.contrib.auth.views import LoginView

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from MyLibrary.accounts.forms import CreateProfileForm
from MyLibrary.common.view_mixins import RedirectToDashboard


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
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()