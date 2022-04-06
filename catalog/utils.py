from .models import Category
from django.db.models import Count


class DataMixin:
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        categoryes = Category.objects.annotate(Count('product'))
        context['categoryes'] = categoryes
        context['logo'] = 'Категории'
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'title' not in context:
            context['title'] = 'Каталог'
        return context

