from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from product_categories.models import ProductCategory
from product_categories.serializers import ProductCategorySerializer

from utilities.viewsets import BaseViewSet

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_flex_fields.views import FlexFieldsMixin
from rest_flex_fields import is_expanded


class ProductCategoriesViewSet(FlexFieldsMixin, BaseViewSet):

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]
    permit_list_expands = ['parent']

    @extend_schema(parameters=[
        OpenApiParameter(name='parent_id',
                         required=False,
                         type=int,
                         description="Parent id filter"),
        OpenApiParameter(name='level_id',
                         required=False,
                         default=0,
                         type=int,
                         description="Level id filter"),
    ])
    def list(self, request: Request) -> Response:
        """Get list of product categories"""

        categories: QuerySet = self.filter_queryset(self.get_queryset())

        # [Filter] Parent id
        parent_id_filter = request.query_params.get('parent_id')

        if parent_id_filter:
            parent_id = int(parent_id_filter)
            categories = categories.filter(parent__id=parent_id)

        # [Filter] Level id
        level_id_filter = request.query_params.get('level_id')

        if level_id_filter:
            level_id = int(level_id_filter)
            categories = categories.filter(level_id=level_id)

        # Expanded Fields
        if is_expanded(request, 'parent'):
            categories = categories.select_related('parent')

        # Paginate
        categories = self.paginate_queryset(categories)

        serializer = self.get_serializer(categories, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        """Get single product category"""

        category = get_object_or_404(ProductCategory, id=pk)
        serializer = self.get_serializer(category)
        return Response(serializer.data)
