from django.db import models

from utilities.models import BaseModel


class ProductCategory(BaseModel):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(max_length=512)
    level_id = models.PositiveSmallIntegerField()
    icon = models.CharField(max_length=512, blank=True, default='')
    slider_image = models.CharField(max_length=512, blank=True, default='')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Product Categories"

    def __str__(self) -> str:
        return self.name
