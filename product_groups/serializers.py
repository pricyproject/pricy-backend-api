from rest_framework import serializers

from product_groups.models import ProductGroup
from rest_flex_fields.serializers import FlexFieldsSerializerMixin


class ProductGroupSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):

    # TODO: Add 'products' default serializer here

    class Meta:
        model = ProductGroup
        fields = '__all__'
        expandable_fields = {
            'products': ('products.ProductSerializer', {'many': True})
        }
