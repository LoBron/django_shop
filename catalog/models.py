from django.db import models

# Create your models here.
class Category(models.Model):
    """Модель категории"""
    name = models.CharField(
        'Название',
        max_length=30,
        unique=True)
    slug = models.SlugField(
        max_length='30',
        unique=True)

    def __str__(self):
        return self.name

