from django.db import models
from django.urls import reverse


class Womens(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField(blank=True)
    photo = models.ImageField('Фотография', upload_to='photos/%Y/%m/%d')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Женщина'
        verbose_name_plural = 'Женщины'

    def __str__(self):
        return self.title

'''    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})'''

class Category(models.Model):
    name = models.CharField('Категория', max_length=100, db_index=True)
    def __str__(self):
        return self.name
