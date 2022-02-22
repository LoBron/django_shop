from django.db import models

# Create your models here.
# from photologue.models import Photo, Gallery

class Section(models.Model):
    """Модель раздела"""
    name = models.CharField('Название раздела', max_length=30, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    """Модель категории"""
    section = models.ForeignKey(Section, verbose_name='Раздел', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Название категории', max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=50)
    # slug = models.SlugField(max_length=30)
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

    def __str__(self):
        return self.title

class Furniture_plugs(models.Model):
    """Заглушки мебельные"""

