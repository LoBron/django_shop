from django.shortcuts import render

# Create your views here.
from catalog.models import *


def show_all_items(request):
    products = Product.objects.all()
    data = {
        'products': products,
        'title': 'Каталог'
    }
    return render(request, 'catalog/catalog_home.html', data)

def show_category(request):
    pass