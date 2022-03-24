from django.views.generic import TemplateView, ListView

from MyLibrary.common.view_mixins import RedirectToDashboard
from MyLibrary.main.models import Book


class IndexView(RedirectToDashboard, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class DashboardView(ListView):
    model = Book
    #form_class =
    template_name = 'main/dashboard.html'
    context_object_name = 'pet_photos'