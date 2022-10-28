from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from catalog.models import Product
from users.models import Address, User


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    address = models.ForeignKey(
        Address,
        verbose_name=_('Address'),
        on_delete=models.SET_NULL,
        null=True
    )
    phone = PhoneNumberField(
        max_length=13,
        help_text='Формат номера телефона +375296812285'
    )
    payment_status = models.ForeignKey(
        'PaymentStatus',
        verbose_name=_('Payment status'),
        on_delete=models.PROTECT
    )
    products = models.ManyToManyField(
        Product,
        through='ProductOrder'
    )
    comment = models.TextField(_('Comment'), default='')


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.PROTECT)
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_('Amount'), default=1)


class Status(models.Model):
    name = models.CharField(_('Status'), max_length=100, unique=True)
    orders = models.ManyToManyField(Order, through='StatusOrder')

    class Meta:
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name


class StatusOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Status'), on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name=_('Order'), on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)


class PaymentStatus(models.Model):
    name = models.CharField(_('Payment status'), max_length=100, unique=True)

    class Meta:
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name
