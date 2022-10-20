import time
from decimal import Decimal
import random
from django.shortcuts import get_object_or_404
from num2words import num2words
from .models import Category, Product
from django.db.models import Count


# import string

class DataMixin:
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 24

    def get_user_context(self, **kwargs):
        context = kwargs
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


def num_to_word(n: int) -> str:
    if n < 0 or n > 99:
        raise ValueError('You must enter a number from 0 to 99')
    num_word = ''
    num = num2words(n).split('-')
    for word in num:
        num_word += word.capitalize()
    return num_word
