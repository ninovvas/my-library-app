from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class AuthorsView(LoginRequiredMixin, ListView):
    pass

class CreateAuthorView(LoginRequiredMixin, CreateView):
    pass

class DetailsAuthorView(LoginRequiredMixin, DetailView):
    pass

class EditAuthorView(LoginRequiredMixin, UpdateView):
    pass

class DeleteAuthorView(LoginRequiredMixin, DeleteView):
    pass