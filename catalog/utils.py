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