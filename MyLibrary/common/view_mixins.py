from django.shortcuts import redirect

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