from django.contrib import admin

# from photologue.admin import GalleryAdmin as GalleryAdminDefault, GalleryAdmin
# from photologue.models import Gallery
# Register your models here.
from catalog.models import Category, Product, Atribut, AtributsGroup, AtributValue, Section


admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Atribut)
admin.site.register(AtributsGroup)
admin.site.register(AtributValue)
# admin.site.register(Gallery, GalleryAdmin)