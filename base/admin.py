from django.contrib import admin
from django.utils.safestring import mark_safe

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import *


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class DeliveryAddressInline(admin.TabularInline):
    model = DeliveryAddress
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('delivered_at',)
    inlines = (OrderItemInline, DeliveryAddressInline)


admin.site.register(Review)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)
    inlines = (ReviewInline,)

    @staticmethod
    @admin.display(description='Предпросмотр')
    def image_preview(obj: Product) -> str:
        return mark_safe(f'<img src="{obj.picture.url}" style="max-height: 150px;">')
