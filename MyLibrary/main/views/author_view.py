from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from MyLibrary.common.view_mixins import RedirectPermissionRequiredMixin
from MyLibrary.main.forms import CreateAuthorForm
from MyLibrary.main.models import Author


class AuthorsView(LoginRequiredMixin, RedirectPermissionRequiredMixin, ListView):
    model = Author
    template_name = 'main/authors.html'
    context_object_name = 'list_authors'
    permission_required = ('main.view_author',)

    # def get_queryset(self):
    #     return Book.objects.filter(
    #         user=self.request.user,
    #     )

class CreateAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    permission_required = ('main.add_author',)
    form_class = CreateAuthorForm
    template_name = 'main/author_create.html'
    success_url = reverse_lazy('authors view')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DetailsAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DetailView):
    permission_required = ('main.view_author',)

class EditAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_author',)

class DeleteAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DeleteView):
    permission_required = ('main.delete_author',)
    