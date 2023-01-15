from admin_anchors import admin_anchor
from django.contrib import admin

from product_categories.models import ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level_id', 'description',
                    'parent_link', 'products_link')
    list_filter = (('parent', admin.RelatedOnlyFieldListFilter), 'level_id')
    search_fields = ('id', 'name', 'description')

    @admin_anchor("parent")
    def parent_link(self, instance: ProductCategory):
        return str(instance.parent)

    @admin_anchor("products")
    def products_link(self, instance: ProductCategory):
        return f"{instance.products.count()} Products"
