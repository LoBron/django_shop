from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db import models

# Create your views here.
from django.views.generic import DetailView, ListView

from catalog.models import Product, Category



def show_catalog(request):
    products = Product.objects.all()
    categoryes = Category.objects.all().order_by('name')
    data = {
        'products': products,
        'categoryes': categoryes,
        'title': 'Каталог',
        'logo': 'Категории',
    }
    return render(request, 'catalog/catalog_home.html', data)

# class CatalogProduct(ListView):
#     model = Product
#     template_name = 'catalog/catalog_home.html'
#     context_object_name = 'categoryes'
#     data = {
#         'products': products,
#         'categoryes': categoryes,
#         'title': 'Каталог',
#         'logo': 'Категории',
#     }
#
#     def get_context_data(self, *, object_list = None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         for i in data:
#
#         context['now'] = timezone.now()
#         return context

def show_category(request, cat_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    products = Product.objects.filter(category=cat.id)
    # if len(products) == 0:
    #     raise Http404()
    data = {
        'products': products,
        'title': cat.name,
        'logo': cat.name,
    }
    return render(request, 'catalog/catalog_category.html', data)

class ProductDetail(DetailView):
    model = Product
    template_name = 'catalog/catalog_category_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
