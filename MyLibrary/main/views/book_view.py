from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin

from MyLibrary.main.forms import SearchBookForm, CreateBookForm
from MyLibrary.main.models import Book
from MyLibrary.common.BookAPI import BookSearch

#LoginRequiredMixin
class CreateBookView(CreateView):
    model = Book
    form_class = CreateBookForm
    template_name = 'main/book_create.html'
    success_url = reverse_lazy('dashboard')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context['title'] = self.request.session['title']
    #     return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        if self.request.session.get('title', False):
            initial['title'] = self.request.session['title']
            try:
                del self.request.session['title']
            except:
                pass

        return initial


#TemplateView
#class SearchBookView(LoginRequiredMixin, FormView):
class SearchBookView(FormView):
    template_name = 'main/book_search.html'
    form_class = SearchBookForm
    success_url = reverse_lazy('add book')
    data = {}

    def form_valid(self, form):
        search_query = form.cleaned_data
        print(f"search_query = {search_query}")
        book_search = BookSearch(search_query['isbn'])
        book_search.make_a_search()
        results = book_search.get_search_results()
        print(f"results = {results}")
        if 'title' in self.request.session:
            del self.request.session['title']
        if results == "no results":
            pass
        else:
            self.request.session['title'] = results[0]['title']

        return super().form_valid(form)


