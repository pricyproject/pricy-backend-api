

from rest_framework import serializers

from product_categories.models import ProductCategory
from rest_flex_fields.serializers import FlexFieldsSerializerMixin


class ProductCategorySerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("__all__")
        expandable_fields = {
            'parent': 'product_categories.ProductCategorySerializer'
        }
