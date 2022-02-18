from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault, GalleryAdmin
from photologue.models import Gallery
# Register your models here.
from catalog.models import Category, Product

admin.site.register(Category, Product)
admin.site.register(Gallery, GalleryAdmin)