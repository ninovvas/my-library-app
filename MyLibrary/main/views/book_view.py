from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin

from MyLibrary.main.forms import SearchBookForm, CreateBookForm, AuthorsBookForm
from MyLibrary.main.models import Book
from MyLibrary.common.BookAPI import BookSearch


book_fields = ['title','authors','description','isbn10','isbn13','page_count','publisher','language']
authors = ['name', 'email']
all_fields = book_fields + authors


#LoginRequiredMixin
class CreateBookView(LoginRequiredMixin, CreateView):
    #model = Book
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#TemplateView
#class SearchBookView(LoginRequiredMixin, FormView):
class SearchBookView(LoginRequiredMixin, FormView):
    template_name = 'main/book_search.html'
    form_class = SearchBookForm
    success_url = reverse_lazy('add book')
    fields = []



    def form_valid(self, form):
        #form.instance.user = self.request.user

        search_query = form.cleaned_data
        print(f"search_query = {search_query}")
        book_search = BookSearch(search_query['isbn'])
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





