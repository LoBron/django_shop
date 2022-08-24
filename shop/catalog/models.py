from django.db import models

# Create your models here.
# from photologue.models import Photo, Gallery
from django.template.defaultfilters import slugify
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    """Модель категории"""
    name = models.CharField('Название категории', max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('URL', max_length=50, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        index_together = (('id', 'slug'),)
        # ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название товара', max_length=200)
    slug = models.SlugField('URL', max_length=200)
    description = models.TextField('Описание', null=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
    availability = models.BooleanField('Наличие', default=True)
    amount = models.PositiveIntegerField('Количество', default=1)
    photo1 = models.CharField('Фото 1', max_length=50)
    photo2 = models.CharField('Фото 2', max_length=50, null=True, blank=True)
    photo3 = models.CharField('Фото 3', max_length=50, null=True, blank=True)
    photo4 = models.CharField('Фото 4', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        index_together = (('id', 'slug'),)
        # ordering = ['-availability', 'category', 'title']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_id': self.pk, 'prod_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)


class Property(models.Model):
    name = models.CharField('Property name', max_length=200, unique=True)
    products = models.ManyToManyField(Product, through='PropertyValue', through_fields=('property', 'product'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('property', kwargs={'property_id': self.pk})


class PropertyValue(models.Model):
    property = models.ForeignKey(Property, verbose_name='Property', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    value = models.CharField('Property value', max_length=200)

    def __str__(self):
        return f'{self.product} - {self.property}: {self.value}'

    class Meta:
        verbose_name = "Property value"
        verbose_name_plural = "Properties values"

# class Cart(models.Model):
#     """Корзина"""
#     session = models.CharField("Сессия пользователя", max_length=500, null=True, blank=True)
#     user = models.ForeignKey(
#         User, verbose_name='Покупатель', on_delete=models.CASCADE, null=True, blank=True
#     )
#     accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзины'
#
#     def __str__(self):
#         return "{}".format(self.user)
