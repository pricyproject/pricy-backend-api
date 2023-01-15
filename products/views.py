from decimal import Decimal
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from django.db.models import F, Sum
from django.db.models.functions import Coalesce

from products.serializers import ProductSerializer
from utilities.viewsets import BaseViewSet
from .models import Product, ProductLinkView, ProductView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_flex_fields.views import FlexFieldsMixin
from rest_flex_fields import is_expanded


class ProductsViewSet(FlexFieldsMixin, BaseViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    permit_list_expands = ['categories', 'shop', 'groups']

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
                             OpenApiExample('Views (descending)', '-views')
                         ],
                         description="Order by a field (+|-)"),
        OpenApiParameter(name='group_id',
                         required=False,
                         type=int,
                         description="Product group id filter"),
    ])
    def list(self, request: Request) -> Response:
        """Get list of product"""

        products: QuerySet = self.filter_queryset(self.get_queryset())

        # [Filter] Min Price
        min_price_filter = request.query_params.get('min_price')

        if min_price_filter:
            min_price = Decimal(min_price_filter)
            products = products.annotate(realprice=F(
                'price') - F('discount')).filter(realprice__gte=min_price)

        # [Filter] Max Price
        max_price_filter = request.query_params.get('max_price')

        if max_price_filter:
            max_price = Decimal(max_price_filter)
            products = products.annotate(realprice=(
                F('price') - F('discount'))).filter(realprice__lte=max_price)

        # [Filter] Shop's Country
        country_filter = request.query_params.get('country')

        if country_filter:
            products = products.filter(shop__country__iexact=country_filter)

        # [Filter] Categories
        categories_filter = request.query_params.getlist('categories', '')

        if categories_filter:
            categories: list[str] = categories_filter
            products = products.filter(
                categories__name__in=categories)

        # [Filter] Minimum Views
        min_views_filter = request.query_params.get('min_views')

        if min_views_filter:
            min_views = int(min_views_filter)
            products = products.annotate(total_views=Coalesce(
                Sum('views__count'), 0)).filter(total_views__gte=min_views)

        # [Filter] Group id
        group_id_filter = request.query_params.get('group_id')

        if group_id_filter:
            group_id = int(group_id_filter)
            products = products.filter(groups__id=group_id)

        # Expanded Fields
        if is_expanded(request, 'categories'):
            products = products.prefetch_related('categories')

        if is_expanded(request, 'shop'):
            products = products.select_related('shop')

        if is_expanded(request, 'groups'):
            products = products.prefetch_related('groups')

        # Ordering & Sort
        ordering = self.get_ordering_value()
        ordering_sign = self.get_ordering_sign()

        match ordering:
            case 'views':
                products = products.annotate(total_views=Coalesce(
                    Sum('views__count'), 0)).order_by(f'{ordering_sign}total_views')

        # Pagination
        products = self.paginate_queryset(products)

        serializer = self.get_serializer(products, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk=None):
        """Get single product"""

        product = get_object_or_404(Product, id=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @extend_schema(request=None,
                   parameters=[
                       OpenApiParameter(name='short_key',
                                        required=True,
                                        type=str,
                                        description='Short key of product')
                   ],
                   responses={status.HTTP_302_FOUND: None,
                              status.HTTP_400_BAD_REQUEST: None})
    @ action(detail=True, methods=['GET'])
    def go(self, request: Request, pk=None) -> Response:

        short_key = request.query_params.get('short_key')

        if not short_key:
            raise ValidationError("The 'short_key' query param is required")

        product = get_object_or_404(Product, id=pk, short_key=short_key)

        link_view = ProductLinkView()
        link_view.product = product
        link_view.client_ip = self.get_client_ip()
        link_view.save()

        return redirect(product.link)

    @ extend_schema(request=None,
                    responses={status.HTTP_204_NO_CONTENT: None,
                               status.HTTP_400_BAD_REQUEST: None,
                               status.HTTP_404_NOT_FOUND: None})
    @ action(detail=True, methods=['POST'])
    def view(self, request: Request, pk=None) -> Response:
        """View a single product"""

        product = get_object_or_404(Product, id=pk)

        client_ip = self.get_client_ip()

        product_view, created = ProductView.objects.get_or_create(
            defaults={'product': product, 'count': 1, 'client_ip': client_ip},
            product=product, client_ip=client_ip)

        if created:
            return Response(status=status.HTTP_204_NO_CONTENT)

        product_view.count += 1
        product_view.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
