from product_categories.serializers import ProductCategorySerializer
from product_groups.serializers import ProductGroupSerializer
from products.models import Product
from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin

from shops.serializers import ShopSerializer


class ProductSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('link',)

        expandable_fields = {
            'shop': ShopSerializer,
            'categories': (ProductCategorySerializer, {'many': True}),
            'groups': (ProductGroupSerializer, {'many': True})
        }
