from admin_anchors import admin_anchor
from django.contrib import admin

from product_groups.models import ProductGroup


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'enable', 'min_price',
                    'max_price', 'currency', 'type', 'products_link', 'created_at')
    list_filter = ('enable', 'brand', 'type', 'currency')
    search_fields = ('id', 'name', 'brand', 'type')

    @admin_anchor("products")
    def products_link(self, instance: ProductGroup):
        return f"{instance.products.count()} Products"
