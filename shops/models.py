from pydoc import describe
from django.db import models

from utilities.models import BaseModel


class ShopWorkField(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        'product_categories.ProductCategory', on_delete=models.RESTRICT)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Shop Work Fields"

    def __str__(self) -> str:
        return self.name


class Shop(BaseModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, default='')
    link = models.URLField(max_length=2048)
    country = models.CharField(max_length=32)
    work_fields = models.ManyToManyField(ShopWorkField, related_name='shops')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Shops"

    def __str__(self) -> str:
        return self.name
