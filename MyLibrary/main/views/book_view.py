from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, FormView, ListView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin, DetailView

from MyLibrary.common.view_mixins import RedirectPermissionRequiredMixin
from MyLibrary.main.forms import SearchBookForm, CreateBookForm, AuthorsBookForm, EditBookForm, DetailsBookForm, \
    DeleteBookForm
from MyLibrary.main.models import Book
from MyLibrary.common.BookAPI import BookSearch


book_fields = ['title','authors','description','isbn10','isbn13','page_count','publisher','language']
authors = ['name', 'email']
all_fields = book_fields + authors


class CreateBookView(LoginRequiredMixin, RedirectPermissionRequiredMixin, CreateView):
    #model = Book
    permission_required = ('main.add_book',)
    form_class = CreateBookForm
    template_name = 'main/book_create.html'
    success_url = reverse_lazy('dashboard')


    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial = self._set_initial_value(initial)
        return initial

    def _set_initial_value(self, initial_obj):
        for field_name in all_fields:
            if self.request.session.get(field_name, ''):
                initial_obj[field_name] = self.request.session[field_name]
                try:
                    del self.request.session[field_name]
                except:
                    pass
        return initial_obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SearchBookView(LoginRequiredMixin, RedirectPermissionRequiredMixin, FormView):
    permission_required = ('main.add_book',)
    template_name = 'main/book_search.html'
    form_class = SearchBookForm
    success_url = reverse_lazy('add book')
    #permission_required = ('MyLibrary.main.add_book',)

    fields = []

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        form.user = self.request.user

        search_query = form.cleaned_data
        print(f"search_query = {search_query}")
        book_search = BookSearch(search_query['input_search'])
        book_search.make_a_search()
        results = book_search.get_search_results()
        print(f"results = {results}")
        #delete previous sessions if exist
        self._reset_all_sessions()
        if results is not None:
            self._set_session_value(results)

        return super().form_valid(form)

    def _set_session_value(self, data: dict):
        for data_key in data.keys():

            if 'authors' == data_key:
                session_key = data_key
                session_value = ", ".join(data['authors'])
            elif 'isbns' == data_key:
                for isbn in data['isbns']:
                    if isbn['type'] == 'ISBN_13':
                        session_key = 'isbn13'
                        session_value = isbn['identifier']
                    elif isbn['type'] == 'ISBN_10':
                        session_key = 'isbn10'
                        session_value = isbn['identifier']
                    else:
                        session_key = ""
                        session_value = ""
                    self.request.session[session_key] = session_value
                    self.fields.append(session_key)
            elif 'publisher' == data_key:
                session_key = data_key
                session_value = data['publisher']
            else:
                session_key = data_key
                session_value = data[data_key]
            if 'isbn13' in self.request.session or 'isbn10' in self.request.session:
                continue
            self.request.session[session_key] = session_value
            self.fields.append(session_key)

        for key, value in self.request.session.items():
            print(f"Sessions: {key, value}")

    def _reset_all_sessions(self):
        for session_key in all_fields:
            if session_key in self.request.session:
                del self.request.session[session_key]


class EditBookView(LoginRequiredMixin,RedirectPermissionRequiredMixin, UpdateView):
    model = Book
    template_name = 'main/book_edit.html'
    form_class = EditBookForm
    permission_required = ('main.change_book',)

    def get_success_url(self):
        return reverse_lazy('details book', kwargs={'pk': self.object.id})


class DetailsBookView(LoginRequiredMixin,RedirectPermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'main/book_details.html'
    form_class = DetailsBookForm
    context_object_name = 'book_details'
    permission_required = ('main.view_book',)


class DeleteBookView(LoginRequiredMixin,RedirectPermissionRequiredMixin, DeleteView):
    model = Book
    template_name = "main/book_delete.html"
    permission_required = ('main.delete_book',)
    success_url = reverse_lazy('dashboard')

    # def get_queryset(self):
    #     owner = self.request.user
    #     return self.model.objects.filter(user=owner)

    # def get_queryset(self, **kwargs):
    #     query = super().get_queryset()
    #     return Book.objects.filter(
    #         user=self.request.user,
    #         authors__book__authors=query.
    #     )

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(pk=self.pk)
    #
    #     return queryset





