from admin_anchors import admin_anchor
from django.contrib import admin
from .models import *


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'link',
                    'country', 'work_fields_link')
    list_filter = ('country', 'work_fields')
    search_fields = ('id', 'name', 'link', 'description')

    @admin_anchor("work_fields")
    def work_fields_link(self, instance: Shop) -> str:
        work_fields = list(instance.work_fields.all())
        return ', '.join((str(work_field)) for work_field in work_fields)


@admin.register(ShopWorkField)
class ShopWorkFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_link', 'shops_link')
    list_filter = ('category', )
    search_fields = ('id', 'name', 'category')

    @admin_anchor("category")
    def category_link(self, instance: ShopWorkField):
        return str(instance.category)

    @admin_anchor("shops")
    def shops_link(self, instance: Shop) -> str:
        shops = list(instance.shops.all())
        return ', '.join((str(shop)) for shop in shops)
