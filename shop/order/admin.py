from django.contrib import admin

from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(StatusOrder)
class StatusOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    pass
