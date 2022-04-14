from .models import Category, Product
from django.db.models import Count


class DataMixin:
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_user_context(self, **kwargs):
        context = kwargs
        # categ = Category.objects.all()
        # context['categ'] = categ
        categoryes = Category.objects.annotate(Count('product'))
        context['categoryes'] = categoryes
        context['logo2'] = 'Параметры'
        if 'logo1' not in context:
            context['logo1'] = 'Категории'
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'title' not in context:
            context['title'] = 'Каталог'
        return context