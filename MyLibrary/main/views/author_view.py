from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from MyLibrary.common.view_mixins import RedirectPermissionRequiredMixin
from MyLibrary.main.models import Author


class AuthorsView(LoginRequiredMixin, RedirectPermissionRequiredMixin, ListView):
    model = Author
    template_name = 'main/authors.html'
    context_object_name = 'list_authors'
    permission_required = ('main.delete_author',)

    # def get_queryset(self):
    #     return Book.objects.filter(
    #         user=self.request.user,
    #     )

class CreateAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    permission_required = ('main.add_author',)
    pass

class DetailsAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DetailView):
    permission_required = ('main.view_author',)

class EditAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_author',)

class DeleteAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DeleteView):
    permission_required = ('main.delete_author',)
    