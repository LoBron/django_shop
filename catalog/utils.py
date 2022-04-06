from .models import Category
from django.db.models import Count


class DataMixin:
    paginate_by = 6

    def get_user_context(self, **kwargs):
        context = kwargs
        categ = Category.objects.all()
        context['categ'] = categ
        categoryes = Category.objects.annotate(Count('product'))
        context['categoryes'] = categoryes
        context['logo1'] = 'Категории'
        context['logo2'] = 'Параметры'
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'title' not in context:
            context['title'] = 'Каталог'
        return context

