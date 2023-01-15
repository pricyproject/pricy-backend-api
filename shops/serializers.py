from .models import Shop, ShopWorkField
from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin


class ShopSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("__all__")
