from django.contrib import admin

from .models import *


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


class StatusInline(admin.StackedInline):
    model = Order.statuses.through
    extra = 1


# order_status
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (StatusInline,)


# @admin.register(StatusOrder)
# class StatusOrderAdmin(admin.ModelAdmin):
#     inlines = (StatusOrderInline,)

admin.site.register(OrderStatus)


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    pass
