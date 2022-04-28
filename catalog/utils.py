from decimal import Decimal
import random
from django.shortcuts import get_object_or_404
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

def add_products_to_base(cat_name, products_in_cat):
    products_added = 0
    if len(products_in_cat) > 0:
        k = 1
        for prod in products_in_cat:
            description = ''
            for prop, value in prod['properties'].items():
                description += f'{prop}: {value}. '
            photos = [None for i in range(4)]
            t = 0
            for photo in prod['photos']:
                photos[t] = f'photos/2022/04/20/{photo.split("/")[-1]}'
                t += 1
            product = Product(
                category=get_object_or_404(Category, name=cat_name),
                name=prod['name'],
                slug=prod['slug'],
                description=description,
                price=Decimal(prod['price']),
                availability=True,
                amount=random.choice([i for i in range(1, 101)]),
                main_photo=photos[0],
                additional_photo_01=photos[1],
                additional_photo_02=photos[2],
                additional_photo_03=photos[3]
            )
            try:
                product.save()
            except Exception as ex:
                print(ex.__annotations__)
                print(f'\n            EXEPTION - Товар {prod["name"]} не добавлен - EXEPTION\n')
                continue
            else:
                products_added += 1
            k += 1
    print(f"            Из {len(products_in_cat)} продуктов добавлено {products_added}")
#
#
# def get_slug(string):
#     dic = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v',
#           'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
#           'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l',
#           'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
#           'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
#           'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'yi',
#           'э': 'e', 'ю': 'yu', 'я': 'ya', ',':'', '.':''}
#
#     symbols = '-/:=_|~* '
#     dic = dict(list(dic.items()) + [(i, '_') for i in symbols])
#     slug = ''
#     cash = {}
#
#     for i in string.lower().strip():
#         print(i)
#         c = cash.get(i)
#         print(c)
#         if c:
#             slug += c
#         else:
#             dic_el = dic.get(i)
#             print(f'{i} - {dic_el}')
#             if dic_el:
#                 slug += dic_el
#                 cash[i] = dic_el
# # `            elif el in string.whitespace.split:
# #                 slug += '_'
# #                 cash[el] = '_'`
#             elif i in 'abcdefghijklmnopqrstuvwxyz' or i in '0123456789':
#                 slug += i
#                 cash[i] = i
#             elif i in string.punctuation:
#                 slug += ''
#                 cash[i] = ''
#             else:
#                 slug += ''
#                 cash[i] = ''
#         print(slug)
#     return slug
#
# print(get_slug('Анкер TGS 8х60/5,0-6,0 ЦЖ,газо-, пенобетон'))

# print(string.ascii_lowercase.split())

# for i in 'abcdefghijklmnopqrstuvwxyz':
#     print(i)