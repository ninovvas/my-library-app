from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

import MyLibrary


class RedirectToDashboard:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')

        return super().dispatch(request, *args, **kwargs)

class RedirectToLogin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login user')

        return super().dispatch(request, *args, **kwargs)


class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('dashboard')

    def handle_no_permission(self):
        messages.error(self.request, 'Yeu do not have permission to create new Book! Please contact the administrator.')
        return redirect(self.get_login_url())