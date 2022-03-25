from django.contrib import admin

# from photologue.admin import GalleryAdmin as GalleryAdminDefault, GalleryAdmin
# from photologue.models import Gallery
# Register your models here.
from catalog.models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Section)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(AtributCategory)
admin.site.register(AtributValue)
# admin.site.register(Gallery, GalleryAdmin)