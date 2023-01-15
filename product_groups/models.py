from uuid import uuid4
from django.db import models
from utilities.models import BaseModel
from products.models import CurrencyChoice


class ProductGroupType(models.TextChoices):
    Normal = "Normal"
    Featured = "Featured"


class ProductGroup(BaseModel):
    uuid = models.UUIDField(unique=True, default=uuid4)
    name = models.CharField(max_length=512)
    brand = models.CharField(max_length=128, blank=True, default='')
    enable = models.BooleanField(default=True)
    currency = models.CharField(max_length=32,
                                default=CurrencyChoice.Euro,
                                choices=CurrencyChoice.choices)
    slug = models.CharField(max_length=1024, default='')
    min_price = models.DecimalField(max_digits=19, decimal_places=4)
    max_price = models.DecimalField(max_digits=19, decimal_places=4)
    type = models.CharField(max_length=32,
                            default=ProductGroupType.Normal,
                            choices=ProductGroupType.choices)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Groups"

    def __str__(self) -> str:
        return self.name
