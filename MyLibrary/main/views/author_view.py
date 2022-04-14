from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from MyLibrary.common.view_mixins import RedirectPermissionRequiredMixin
from MyLibrary.main.forms import CreateAuthorForm, DetailsBookForm, DetailsAuthorForm, EditAuthorForm
from MyLibrary.main.models import Author, Book


class AuthorsView(LoginRequiredMixin, RedirectPermissionRequiredMixin, ListView):
    model = Author
    template_name = 'main/authors.html'
    context_object_name = 'list_authors'
    permission_required = ('main.view_author',)


class CreateAuthorView(LoginRequiredMixin,RedirectPermissionRequiredMixin, CreateView):
    permission_required = ('main.add_author',)
    form_class = CreateAuthorForm
    template_name = 'main/author_create.html'
    success_url = reverse_lazy('authors view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DetailsAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DetailView):
    permission_required = ('main.view_author',)
    model = Author
    template_name = 'main/author_details.html'
    form_class = DetailsAuthorForm
    context_object_name = 'author_details'

    def get_context_data(self, **kwargs):
        context = super(DetailsAuthorView, self).get_context_data()
        author_has_books = Book.objects.filter(authors__id=self.object.id)
        context['author_has_books'] = author_has_books

        return context


class EditAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    permission_required = ('main.change_author',)
    model = Author
    template_name = 'main/author_edit.html'
    form_class = EditAuthorForm

    def get_success_url(self):
        return reverse_lazy('details author', kwargs={'pk': self.object.id})


class DeleteAuthorView(LoginRequiredMixin, RedirectPermissionRequiredMixin,  DeleteView):
    permission_required = ('main.delete_author',)
    