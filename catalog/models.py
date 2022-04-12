from django.db import models

# Create your models here.
# from photologue.models import Photo, Gallery
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    """Модель категории"""
    name = models.CharField('Название категории', max_length=30, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField('URL', max_length=30, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        # ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class AtributCategory(models.Model):
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    name = models.CharField('Название атрибута', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    # def get_absolute_url(self):
    #     return reverse('atribut', kwargs={'atribut_slug': self.slug})

class AtributValue(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    atribut_category = models.ForeignKey(AtributCategory, verbose_name='Атрибут категории', on_delete=models.CASCADE)
    value = models.CharField('Значение атрибута', max_length=100)
    def __str__(self):
        return self.atribut_category
    class Meta:
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"

class Product(models.Model):
    """Модель товара"""
    category = TreeForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField('Название товара', max_length=50)
    slug = models.SlugField(max_length=30, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField('Описание')
    price = models.FloatField('Цена', default=0)
    availability = models.BooleanField('Наличие', default=True)
    amount = models.PositiveIntegerField('Количество', default=0)
    main_photo = models.ImageField("Главная фотография", upload_to='photos/%Y/%m/%d')
    additional_photo_01 = models.ImageField("Доп фото 1", upload_to='photos/%Y/%m/%d', null=True, blank=True)
    additional_photo_02 = models.ImageField("Доп фото 2", upload_to='photos/%Y/%m/%d', null=True, blank=True)
    additional_photo_03 = models.ImageField("Доп фото 3", upload_to='photos/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        # ordering = ['-availability', 'category', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})


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