from django.contrib import admin
from admin_anchors import admin_anchor
from products.models import Product
from .models import ProductCrawlLog, ProductLinkView, ProductPriceLog, ProductView


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'enable',
                    'link', 'shop_link', 'created_at')
    list_filter = (('shop', admin.RelatedOnlyFieldListFilter),
                   'enable', 'brand')
    search_fields = ('id', 'name', 'brand')

    @admin_anchor("shop")
    def shop_link(self, instance: Product):
        return str(instance.shop)


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'count', 'client_ip', 'updated_at')
    list_filter = ('client_ip', 'updated_at')
    search_fields = ('id', 'product__name', 'client_ip')

    @admin_anchor("product")
    def product_link(self, instance: ProductView):
        return str(instance.product)


@admin.register(ProductPriceLog)
class ProductPriceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'price', 'discount', 'updated_at')
    list_filter = ('updated_at', )
    search_fields = ('id', 'product__name')

    @admin_anchor("product")
    def product_link(self, instance: ProductPriceLog):
        return str(instance.product)


@admin.register(ProductCrawlLog)
class ProductCrawlLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'crawl_id',
                    'crawl_time', 'updated_at')
    list_filter = ('crawl_id', 'updated_at')
    search_fields = ('id', 'product__name', 'crawl_id')

    @admin_anchor("product")
    def product_link(self, instance: ProductCrawlLog):
        return str(instance.product)


@admin.register(ProductLinkView)
class ProductLinkViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'client_ip', 'created_at')
    list_filter = ('client_ip', 'created_at')
    search_fields = ('id', 'product__name', 'client_ip')

    @admin_anchor("product")
    def product_link(self, instance: ProductLinkView):
        return str(instance.product)
