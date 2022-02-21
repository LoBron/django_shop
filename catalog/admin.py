from django.contrib import admin

# from photologue.admin import GalleryAdmin as GalleryAdminDefault, GalleryAdmin
# from photologue.models import Gallery
# Register your models here.
from catalog.models import Category, Product, Photo



admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Photo)
# admin.site.register(Gallery, GalleryAdmin)