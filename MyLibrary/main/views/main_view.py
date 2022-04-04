from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

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
        )

    # def detail(request, place_id):
    #     place = Place.objects.get(pk=place_id)
    #     areas = place.area.all()
    #
    #     return render_to_response('detail.html', {
    #         "place": place,
    #         "areas": areas,
    #     })
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['books'] = self.books
    #     context['author'] = self.
    #     return context