from django.db import models

# Create your models here.
# from photologue.models import Photo, Gallery

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

class Photo(models.Model):
    """Фотография товара"""
    photo = models.ImageField("Фотография", upload_to='photos/%Y/%m/%d')


    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    price = models.FloatField('Цена', default=0)
    slug = models.SlugField(max_length=30)
    availability = models.BooleanField('Наличие', default=True)
    amount = models.IntegerField('Количество', default=0)
    photos = models.ManyToManyField(Photo, verbose_name='Фотографии')

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title