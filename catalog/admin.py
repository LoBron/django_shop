from django.contrib import admin
from django.contrib.admin import register
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from .models import *

@register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class AtributCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Product, ProductAdmin)


class CategoryAdmin(DraggableMPTTAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 30
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)


admin.site.register(AtributCategory, AtributCategoryAdmin)
admin.site.register(AtributValue)
# admin.site.register(Gallery, GalleryAdmin)