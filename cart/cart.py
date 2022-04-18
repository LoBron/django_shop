from decimal import Decimal
from django.conf import settings
from website.catalog.models import Product

class Cart(object):

    def __init__(self, request):
        """Инициализируем корзину"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session.get[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавляем товар в корзину или обновляем его количество"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Сохраняем товар"""
        self.session.modified = True

    def remote(self, product):
        """Удаляем товар"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()