from django.contrib import admin

# from photologue.admin import GalleryAdmin as GalleryAdminDefault, GalleryAdmin
# from photologue.models import Gallery
# Register your models here.
from catalog.models import *


admin.site.register(Section)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(AtributCategory)
admin.site.register(AtributValue)
# admin.site.register(Gallery, GalleryAdmin)