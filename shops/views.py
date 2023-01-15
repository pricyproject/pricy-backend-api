from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from django.db.models.query import QuerySet

from utilities.viewsets import BaseViewSet

from .serializers import ShopSerializer
from .models import Shop
from rest_flex_fields.views import FlexFieldsMixin


class ShopsViewSet(FlexFieldsMixin, BaseViewSet):

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]
    permit_list_expands = []

    def list(self, request: Request) -> Response:
        """Get list of shops"""

        shops: QuerySet = self.filter_queryset(self.get_queryset())

        # Paginate
        shops = self.paginate_queryset(shops)

        serializer = self.get_serializer(shops, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        """Get single shop"""

        shop = get_object_or_404(Shop, id=pk)
        serializer = self.get_serializer(shop)
        return Response(serializer.data)
