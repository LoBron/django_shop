import random
from decimal import Decimal

from django.shortcuts import get_object_or_404

import threading
import time
import concurrent.futures
import requests
from bs4 import BeautifulSoup as BS

from catalog.models import Category, Product


def add_cat_to_base(category, parent=None):
    slug = category["slug"]
    if category["slug"] == 'надо доработать':
        slug = f"slug_{int(time.time() * 1000)}"
    cat = Category(
        name=category['name'],
        parent=parent,
        slug=slug
    )
    cat.save()
    print(f'Категория - {category["name"]} - добавлена')

def get_categories_info(main_url):
    """Возвращает список с данными(словарями) о категориях"""
    categories_info = []
    response_obj = requests.get(main_url)
    html_page = BS(response_obj.content, 'html.parser')
    items0_list = html_page.select('.main-menu > .top_level > li')

    for item0 in items0_list[1:2]: #items0_list: #####################
        cat0_name = item0.find_all('span')[0].text.strip()
        if cat0_name in ['Фасады', 'Фасади']:
            continue
        else:
            cat_level_0 = {}
            cat_level_0["name"] = cat0_name
            cat_level_0["slug"] = 'надо доработать'
            cat_level_0["categories_level_1"] = []
            add_cat_to_base(category=cat_level_0)

            items1_list = item0.select('.hidden-label > div')
            parent_1 = get_object_or_404(Category, name=cat_level_0["name"])
            for item1 in items1_list[:]: #items1_list: #####################
                if len(item1) > 0:
                    links = item1.find_all('a')
                    cat1_name = links[0].text.strip()
                    if cat1_name in ['Мойки из искусственного камня  Belterno', 'Мийки зі штучного каменю  Belterno']:
                        continue
                    else:
                        cat_level_1 = {}
                        cat_level_1["name"] = cat1_name
                        href_list_1 = links[0]["href"].split("/")
                        cat_level_1["href"] = f'/{href_list_1[-3]}/{href_list_1[-2]}/'
                        cat_level_1["slug"] = cat_level_1["href"].split('/')[-2]
                        cat_level_1["categories_level_2"] = []
                        add_cat_to_base(category=cat_level_1, parent=parent_1)

                        if len(links) > 1:
                            parent_2 = get_object_or_404(Category, name=cat_level_1["name"])
                            for n in range(1, len(links)): #range(1, len(links)):  #####################
                                cat_level_2 = {}
                                cat_level_2["name"] = links[n].text.strip()
                                href_list_2 = links[n]["href"].split("/")
                                cat_level_2["href"] = f'/{href_list_2[-3]}/{href_list_2[-2]}/'
                                cat_level_2["slug"] = cat_level_2["href"].split('/')[-2]
                                cat_level_1["categories_level_2"].append(cat_level_2)
                                add_cat_to_base(category=cat_level_2, parent=parent_2)

                        cat_level_0["categories_level_1"].append(cat_level_1)
            categories_info.append(cat_level_0)
    print('Cписок с данными о категориях создан\n')
    return categories_info

def add_products_to_base(cat_name, products_in_cat):
    products_added = 0
    category = get_object_or_404(Category, name=cat_name)
    if len(products_in_cat) > 0:
        k = 1
        time_add_products = 0
        time_work_base = 0
        for prod in products_in_cat:
            timer_cycle = time.time()
            description = ''
            for prop, value in prod['properties'].items():
                description += f'{prop}: {value}. '
            photos = [None for i in range(4)]
            t = 0
            for photo in prod['photos']:
                photos[t] = f'photos/2022/04/20/{photo.split("/")[-1]}'
                t += 1
            product = Product(
                category=category,
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
            timer_add = time.time()
            try:
                product.save()
            except Exception as ex:
                print(ex)
                print(f'\n            EXEPTION - Товар {prod["name"]} не добавлен - {ex}\n')
                continue
            else:
                products_added += 1
            k += 1
            time_add_products += time.time()-timer_cycle
            time_work_base += time.time() - timer_add
        print(f"            Время на добавление товаров - {time_add_products}, время работы базы - {time_work_base}, время обработки - {time_add_products - time_work_base}")
    print(f"            Из {len(products_in_cat)} продуктов добавлено {products_added}")


def add_products_data(data, main_url, path_to_download):
    """Добавляет к данным о категоряих данные об их товарах и возвращает полученный список с категориями"""
    for i in range(1): #range(len(data)):
        for j in range(len(data[i].get("categories_level_1"))):
            if len(data[i].get("categories_level_1")[j].get("categories_level_2")) > 0:
                for k in range(len(data[i].get("categories_level_1")[j].get("categories_level_2"))):
                    url = main_url + data[i].get("categories_level_1")[j].get("categories_level_2")[k]['href']
                    print(f'Добавляем список с данными о товарах внутри категории {data[i].get("categories_level_1")[j].get("categories_level_2")[k]["name"]}')
                    data[i].get("categories_level_1")[j].get("categories_level_2")[k]['products'] = get_products_data(category_url=url, path_to_download=path_to_download)
                    add_products_to_base(cat_name=data[i].get("categories_level_1")[j].get("categories_level_2")[k]['name'], products_in_cat=data[i].get("categories_level_1")[j].get("categories_level_2")[k]['products'])
                    print(f'Добавили в категорию {data[i].get("categories_level_1")[j].get("categories_level_2")[k]["name"]} товары в количестве {len(data[i].get("categories_level_1")[j].get("categories_level_2")[k]["products"])} шт\n')
            else:
                url = main_url + data[i].get("categories_level_1")[j]['href']
                print(f'Добавляем список с данными о товарах внутри категории {data[i].get("categories_level_1")[j]["name"]}')
                data[i].get("categories_level_1")[j]['products'] = get_products_data(category_url=url, path_to_download=path_to_download)
                add_products_to_base(cat_name=data[i].get("categories_level_1")[j]['name'], products_in_cat=data[i].get("categories_level_1")[j]['products'])
                print(f'Добавили в категорию {data[i].get("categories_level_1")[j]["name"]} товары в количестве {len(data[i].get("categories_level_1")[j]["products"])} шт\n')
    return data

def get_products_data(category_url, path_to_download):
    """Возвращает список с данными о товарах внутри категории"""
    response_pages_list = get_response_pages(category_url=category_url)
    print(f'    получили responces в количестве {len(response_pages_list)} шт')

    items_url_list = get_items_urls(response_pages_list)
    print(f'    получили items_urls товаров в количестве {len(items_url_list)} шт')

    if len(items_url_list) > 0:

        response_items_list = get_items_responses(items_url_list)
        print(f'    получили response_items товаров в количестве {len(response_items_list)} шт')

        products_data_list = get_items_data(response_items_list, path_to_download)
        print(f'    получили products_data в количестве {len(products_data_list)} шт')

        return products_data_list
    return []

def get_response_pages(category_url):
    """Возвращает список response обьектов со страницами пагинатора внутри категории"""
    response_page_list = []
    n = 1
    while True:
        response_page = requests.get(f'{category_url}page-{n}/')
        if response_page.status_code == 200: #in range(200, 207):   #####################
            response_page_list.append(response_page)
            # print(f'страница {n} добавлена')
            n += 1
        else:
            break
    return response_page_list

# def get_category_pages(name_category, pages):
#     response_page_list = []
#     with concurrent.futures.ThreadPoolExecutor(max_workers=pages) as executor:
#         timer_0 = time.time()
#         future_list = [executor.submit(get_category_page, name_category, page) for page in range(1, pages + 1)]
#         for future in concurrent.futures.as_completed(future_list):
#             response_page_list.append(future.result())
#             print(f"1) время выполнения - {time.time() - timer_0}")
#         print(f"1) время выполнения ФУНКЦИИ - {time.time() - timer_0}\n")
#     return response_page_list

def get_items_urls(response_page_list):
    """Возвращает список URL адресов всех товаров внутри категории"""
    items_url_list = []
    if len(response_page_list) > 0:
        for response_page in response_page_list:
            html = BS(response_page.content, 'html.parser')
            items = html.select('.product_prewiew')
            if len(items):
                for item in items:
                    product = item.select('a')
                    items_url_list.append(f"https://viyar.ua{product[0].get('href')}")
    return items_url_list

def get_item_response(item_url):
    """Возвращает response обьект на product_detail"""
    return requests.get(item_url)

def get_items_responses(items_url_list):
    """Возвращает список response обьектов на все товары внутри категории"""
    items_response_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_list = [executor.submit(get_item_response, item_url) for item_url in items_url_list]
        for future in concurrent.futures.as_completed(future_list):
            items_response_list.append(future.result())
    return items_response_list

def get_item_data(item_response, path_to_download):
    """Возвращает данные о товаре и загружает его фотографии в path_to_download"""
    item_data = {}
    item_html = BS(item_response.content, 'html.parser')
    code = ''
    for i in range(5, random.choice([j for j in range(6, 11)])):
        code += random.choice([str(k) for k in range(0, 10)])
    item_data['name'] = get_name(item_html, code)
    # print(f"object '{item_data['name']}' added")
    item_data['slug'] = get_slug(item_response, code)
    item_data['price'] = get_price(item_html)
    item_data['properties'] = get_properties(item_html)
    item_data['photos'] = get_photos_urls(item_data['name'], item_html)
    download_photos(item_data.get('photos'), path_to_download)
    # print(f"object '{item_data['name']}' added")
    return item_data

# def add_items_data(response_items, path):
#     """https://docs.python.org/3.8/library/concurrent.futures.html#threadpoolexecutor"""
#     items_data = []
#     with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
#         future_list = [executor.submit(add_item_data, response_item, path) for response_item in response_items]
#         for future in concurrent.futures.as_completed(future_list):
#             items_data.append(future.result())
#     return items_data
def get_items_data(items_response_list, path_to_download):
    """Возврашает список данных о товарах и загружает их фотографии в path_to_download"""
    items_data = []
    for item_response in items_response_list:
        items_data.append(get_item_data(item_response, path_to_download))
    return items_data

def get_name(item_html, code):
    """Возвращает наименование товара"""
    try:
        name = item_html.select('.product_name > h1 > b')[0].text.strip()
    except Exception:
        return f'Exeption {code}'
    else:
        return name

def get_slug(item_response, code):
    try:
        url = item_response.url
    except Exception:
        return f'exeption_{code}'
    else:
        return url.split('/')[-2]

def get_price(item_html):
    """Возвращает стоимость товара за единицу"""
    try:
        try:
            price = float(item_html.select('span.price')[0].text.strip())
        except ValueError:
            price = ''
            list_p = item_html.select('span.price')[0].text.strip().split()
            for i in list_p:
                price += i
            price = float(price)
    except Exception:
        return random.choice(range(1700, 2500, 3))
    else:
        return price


def get_properties(item_html):
    """Возвращает характеристики товара"""
    properties = {}
    prop_list = item_html.select('div.charakters > ul.properties > li')
    n = 1
    try:
        for prop in prop_list:
            if n <= len(prop_list) / 2:
                property = prop.text.split(': ')
                properties[property[0]] = property[1].lower()
                n += 1
            else:
                break
    except Exception as ex:
        properties[f'Exception - {ex}'] = 'свойства не добавлены'
    return properties

def get_photos_urls(name, item_html):
    """Возвращает список url адресов фотографий товара"""
    photos_url_list = []
    for n in range(1, 5):
        try:
            if n == 1:
                photo = item_html.find_all('img', alt=name)
            else:
                photo = item_html.find_all('img', alt=name + ' — фото' + str(n))
            photo_url = f"https://viyar.ua{photo[0].get('src')}"
            photos_url_list.append(photo_url)
        except IndexError:
            break
    return photos_url_list

def download_photos(photos_url_list, path):
    """Запускает потоки и загружает в них фотографии товара"""
    if photos_url_list:
        for photo_url in photos_url_list:
            threading.Thread(target=download_photo, args=(photo_url, path)).start()

def download_photo(photo_url, path):
    """Загружает фотографию"""
    root = path + photo_url.split('/')[-1]
    p = requests.get(photo_url)
    img = open(root, "wb")
    img.write(p.content)
    img.close()
     # print(f"Загружено фото {n}")
