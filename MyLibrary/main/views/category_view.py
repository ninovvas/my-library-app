from django.views.generic import ListView


class CategoryView(ListView):
    # form_class =
    template_name = 'admin/category_view.html'


