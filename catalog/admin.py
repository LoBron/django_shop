from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, ProductAdmin)


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 30
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CustomMPTTModelAdmin)


admin.site.register(AtributCategory)
admin.site.register(AtributValue)
# admin.site.register(Gallery, GalleryAdmin)