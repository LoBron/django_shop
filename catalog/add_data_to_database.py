import time
from decimal import Decimal
import random

from .parser.utils import get_categories_info, add_products_data
from .utils import add_products_to_base, add_category_to_base
from django.shortcuts import redirect, get_object_or_404
from catalog.models import Product, Category
from .data import data
from .parser import utils

def categories_save(request):
    main_url = 'https://viyar.ua'
    path_to_download = 'D:/Jango projects/web_app_02/website/media/photos/2022/04/20/'

    data = get_categories_info(main_url)

    add_products_data(data, main_url, path_to_download)
    # for cat_0 in data:
    #     add_category_to_base(category=cat_0)
    #
    #     parent_1 = get_object_or_404(Category, name=cat_0['name'])
    #     for cat_1 in cat_0.get('categories_level_1'):
    #         add_category_to_base(category=cat_1, parent=parent_1)
    #
    #         if len(cat_1['categories_level_2']) > 0:
    #             parent_2 = get_object_or_404(Category, name=cat_1['name'])
    #             for cat_2 in cat_1['categories_level_2']:
    #                 add_category_to_base(category=cat_2, parent=parent_2)
    #
    #                 add_products_to_base(cat_name=cat_2['name'], products_in_cat=cat_2['products'])
    #         else:
    #             add_products_to_base(cat_name=cat_1['name'], products_in_cat=cat_1['products'])
    return redirect('cart_clear')


