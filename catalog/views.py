from django.http import Http404
from django.shortcuts import render

# Create your views here.
from catalog.models import *


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

def show_category(request, cat_id):
    products = Product.objects.filter(category=cat_id)
    # if len(products) == 0:
    #     raise Http404()

    cat = Category.objects.get(pk=cat_id)

    data = {
        'products': products,
        'title': cat.name,
        'logo': cat.name,
    }
    return render(request, 'catalog/catalog_category.html', data)