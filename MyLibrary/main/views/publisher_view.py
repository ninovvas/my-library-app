from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from MyLibrary.common.view_mixins import RedirectPermissionRequiredMixin
from MyLibrary.main.forms import DetailsPublisherForm, CreatePublisherForm, EditPublisherForm
from MyLibrary.main.models import Publisher, Book


class PublishersView(LoginRequiredMixin, RedirectPermissionRequiredMixin, ListView):
    model = Publisher
    template_name = 'main/publishers.html'
    context_object_name = 'list_publishers'
    permission_required = ('main.view_publisher',)


class CreatePublisherView(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    template_name = 'main/publisher_create.html'

    permission_required = ('main.add_publisher',)
    form_class = CreatePublisherForm
    success_url = reverse_lazy('publishers view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DetailsPublisherView(LoginRequiredMixin, RedirectPermissionRequiredMixin, DetailView):

    permission_required = ('main.view_publisher',)
    model = Publisher
    template_name = 'main/publisher_details.html'
    form_class = DetailsPublisherForm
    context_object_name = 'publisher_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        author_has_books = Book.objects.filter(publisher_id=self.object.id)
        context['publisher_has_books'] = author_has_books

        return context


class EditPublisherView(LoginRequiredMixin, RedirectPermissionRequiredMixin, UpdateView):
    template_name = 'main/publisher_edit.html'

    permission_required = ('main.change_publisher',)
    model = Publisher
    form_class = EditPublisherForm

    def get_success_url(self):
        return reverse_lazy('details publisher', kwargs={'pk': self.object.id})


