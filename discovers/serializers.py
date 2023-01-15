from rest_framework import serializers

from .models import HomeDiscover
from rest_flex_fields.serializers import FlexFieldsSerializerMixin


class HomeDiscoverSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = HomeDiscover
        fields = ("__all__")
