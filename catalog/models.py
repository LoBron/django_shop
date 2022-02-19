from django.db import models

# Create your models here.
from photologue.models import Photo, Gallery


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(
        'Название',
        max_length=30,
        unique=True)
    slug = models.SlugField(
        max_length=30,
        unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена', default=0)
    slug = models.SlugField(max_length=30)
    availability = models.BooleanField('Наличие', default=True)
    amount = models.IntegerField('Количество', default=0)
    photo = models.OneToOneField(
        Photo,
        verbose_name='Главная фотография',
        on_delete=models.SET_NULL,
        null=True)
    gallery = models.ForeignKey(
        Gallery,
        verbose_name='Фотографии',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title