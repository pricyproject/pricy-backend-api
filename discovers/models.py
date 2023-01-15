from django.db import models

from utilities.models import BaseModel
from django.db import models


class HomeDiscover(BaseModel):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, default='', blank=True)
    link = models.URLField(max_length=2048)
    image = models.CharField(max_length=2048, blank=True, default='')
    background_image = models.CharField(
        max_length=2048, blank=True, default='')
    button_title = models.CharField(max_length=32, default='Discover')

    class Meta(BaseModel.Meta):
        verbose_name_plural = "Home Discovers"

    def __str__(self) -> str:
        return self.title
