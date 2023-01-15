from typing import Iterable, Optional
from uuid import uuid4
from django.db import models
from utilities.models import BaseModel
from django.contrib.postgres.fields import ArrayField

from products.utils import generate_short_key


class CurrencyChoice(models.TextChoices):
    Pound = "Pound"
    Dollar = "Dollar"
    Euro = "Euro"


class ProductStatus(models.TextChoices):
    Draft = 'Draft'
    Published = 'Published'
    Deleted = 'Deleted'


class Product(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid4)
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    discount = models.DecimalField(max_digits=19, decimal_places=4)
    link = models.URLField(max_length=2048)
    brand = models.CharField(max_length=128, blank=True, default='')
    currency = models.CharField(max_length=32,
                                default=CurrencyChoice.Euro,
                                choices=CurrencyChoice.choices)
    tags = ArrayField(models.CharField(
        max_length=512), blank=True, default=list)
    enable = models.BooleanField(default=True)
    original_image = models.CharField(max_length=2048, default='')
    shop = models.ForeignKey('shops.Shop', on_delete=models.PROTECT)
    categories = models.ManyToManyField(
        'product_categories.ProductCategory', related_name='products')
    slug = models.SlugField(max_length=1024, default='', unique=True)
    description = models.TextField(blank=True, default='')
    color = models.CharField(max_length=256, default='', blank=True)
    groups = models.ManyToManyField(
        'product_groups.ProductGroup', related_name="products")
    short_key = models.CharField(max_length=16, unique=True, null=True)

    status = models.CharField(
        max_length=32, choices=ProductStatus.choices, default=ProductStatus.Published)

    need_crawl = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: Optional[str] = ..., update_fields: Optional[Iterable[str]] = ...) -> None:

        if not self.short_key:
            self.short_key = generate_short_key()

        return super().save(force_insert, force_update, using, update_fields)


class ProductView(BaseModel):
    count = models.PositiveIntegerField(default=1)
    client_ip = models.GenericIPAddressField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='views')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Views"


class ProductPriceLog(BaseModel):
    price = models.DecimalField(max_digits=19, decimal_places=4)
    discount = models.DecimalField(max_digits=19, decimal_places=4)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_logs')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Price Logs"


class ProductCrawlLog(BaseModel):
    crawl_time = models.DateTimeField()
    crawl_id = models.CharField(max_length=256, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='crawl_logs')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Crawl Logs"


class ProductLinkView(BaseModel):
    client_ip = models.GenericIPAddressField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='link_views')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Link Views"
