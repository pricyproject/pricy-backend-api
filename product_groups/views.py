from decimal import Decimal
from django.db.models import Sum, QuerySet, Count
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from product_groups.models import ProductGroup, ProductGroupType
from utilities.search_index import SearchIndex, SearchIndexNames
from product_groups.serializers import ProductGroupSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from utilities.viewsets import BaseViewSet
from rest_flex_fields.views import FlexFieldsMixin
from rest_flex_fields import is_expanded


class ProductGroupsViewSet(FlexFieldsMixin, BaseViewSet):

    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    permission_classes = [permissions.AllowAny]
    permit_list_expands = ['products']

    @extend_schema(parameters=[
        OpenApiParameter(name='min_price',
                         required=False,
                         type=Decimal,
                         description='Minimum price filter'),
        OpenApiParameter(name='max_price',
                         required=False,
                         type=Decimal,
                         description='Maximum price filter'),
        OpenApiParameter(name='country',
                         required=False,
                         type=str,
                         description="Shop country filter"),
        OpenApiParameter(name='categories',
                         required=False,
                         type=str,
                         description="List of categories filter"),
        OpenApiParameter(name='min_views',
                         required=False,
                         type=int,
                         description="Minimum product views filter"),
        OpenApiParameter(name='ordering',
                         required=False,
                         type=str,
                         examples=[
                             OpenApiExample('', ''),
                             OpenApiExample('Views', 'views'),
                             OpenApiExample('Views (descending)', '-views'),
                             OpenApiExample('Link Views', 'link_views'),
                             OpenApiExample(
                                 'Link Views (descending)', '-link_views'),
                         ],
                         description="Order by a field (+|-)"),
        OpenApiParameter(name='type',
                         required=False,
                         type=str,
                         examples=[OpenApiExample('', '')] + [
                             OpenApiExample(groupType, value=groupType.value)
                             for groupType in ProductGroupType
                         ],
                         description="Type of product group"),
    ])
    def list(self, request: Request) -> Response:
        """Get list of product groups"""

        product_groups: QuerySet = self.filter_queryset(self.get_queryset())

        # [Filter] Min Price
        min_price_filter = request.query_params.get('min_price')

        if min_price_filter:
            min_price = Decimal(min_price_filter)
            product_groups = product_groups.filter(min_price__gte=min_price)

        # [Filter] Max Price
        max_price_filter = request.query_params.get('max_price')

        if max_price_filter:
            max_price = Decimal(max_price_filter)
            product_groups = product_groups.filter(min_price__lte=max_price)

        # [Filter] Shop's Country
        country_filter = request.query_params.get('country')

        if country_filter:
            product_groups = product_groups.filter(
                products__shop__country__iexact=country_filter)

        # [Filter] Categories
        categories_filter = request.query_params.getlist('categories', '')

        if categories_filter:
            categories: list[str] = categories_filter
            product_groups = product_groups.filter(
                products__categories__name__in=categories)

        # [Filter] Minimum Views
        min_views_filter = request.query_params.get('min_views')

        if min_views_filter:
            min_views = int(min_views_filter)
            product_groups = product_groups.annotate(total_views=Coalesce(
                Sum('products__views__count'), 0)).filter(total_views__gte=min_views)

        # [Filter] Group type
        type_filter = request.query_params.get('type')

        if type_filter:
            product_groups = product_groups.filter(type=type_filter)

        if is_expanded(request, 'products'):
            product_groups = product_groups.prefetch_related('products')

        # Ordering & Sort
        ordering = self.get_ordering_value()
        ordering_sign = self.get_ordering_sign()

        match ordering:
            case 'views':
                product_groups = product_groups.annotate(total_views=Coalesce(
                    Sum('products__views__count'), 0)).order_by(f'{ordering_sign}total_views')
            case 'link_views':
                product_groups = product_groups.annotate(total_link_views=Coalesce(
                    Count('products__link_views'), 0)).order_by(f'{ordering_sign}total_link_views')

        # Pagination
        product_groups = self.paginate_queryset(product_groups)

        serializer = self.get_serializer(product_groups, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk=None):
        """Get single product group"""

        product_group = get_object_or_404(ProductGroup, id=pk)
        serializer = self.get_serializer(product_group)
        return Response(serializer.data)

    @extend_schema(parameters=[
        OpenApiParameter(name='q',
                         required=True,
                         type=str,
                         description='Search query'),
    ],
        responses={
            status.HTTP_200_OK: ProductGroupSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: None
    })
    @action(detail=False, methods=['GET'])
    def search(self, request: Request) -> Response:
        """Search through product groups"""

        q = request.query_params.get('q')

        if not q:
            raise ValidationError("The 'q' parameter is required.")

        search_index = SearchIndex(SearchIndexNames.product_groups)

        ids = search_index.search(
            q, limit=self.page_size, offset=self.page_number - 1)

        product_groups: QuerySet = self.get_queryset()
        product_groups = product_groups.filter(id__in=ids)

        # Pagination
        product_groups = self.paginate_queryset(product_groups)

        serializer = self.get_serializer(product_groups, many=True)
        return self.get_paginated_response(serializer.data)
