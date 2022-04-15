from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models import Q

from MyLibrary.common.view_mixins import RedirectToDashboard
from MyLibrary.main.models import Book, Author


class IndexView(RedirectToDashboard, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class DashboardView(LoginRequiredMixin, ListView):
    model = Book
    #form_class =
    #books = Book.objects.all()
    template_name = 'main/dashboard.html'
    context_object_name = 'list_books'

    def get_queryset(self):
        return Book.objects.filter(
            user=self.request.user,
        ).order_by('title')


class UserSearchBookView(ListView):
    model = Book
    template_name = 'main/result_book_search.html'
    context_object_name = 'result_search'

    def get_queryset(self):
        search_text = self.request.GET.get('q')
        if search_text:
            return Book.objects.filter(
                Q(user=self.request.user) & Q(title__icontains=search_text) | Q(isbn10__icontains=search_text) |
                Q(isbn13__icontains=search_text)
            )
        return None
