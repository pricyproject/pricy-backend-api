from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
import logging


class BaseViewSet(GenericViewSet):

    # page_size = api_settings.PAGE_SIZE

    # def get_paginated_queryset(self, queryset: Any) -> Any:
    #     param = self.request.query_params.get('page')
    #     page = int(param) if param is not None and param.isdigit() else 1
    #     page_index = (page - 1) * self.page_size

    #     return queryset[page_index: page_index + self.page_size]

    def get_ordering_value(self) -> str:
        ordering = self.request.query_params.get('ordering')

        if ordering is None:
            return None

        if ordering[0] == '-' or ordering[0] == '+':
            return ordering[1:]

        return ordering

    def get_ordering_sign(self) -> str:
        ordering = self.request.query_params.get('ordering')

        if ordering is None:
            return None

        if ordering[0] == '-':
            return '-'

        return ''

    def get_client_ip(self) -> str:
        if settings.USE_X_REAL_IP:
            x_real_ip = self.request.META.get('HTTP_X_REAL_IP')

            if x_real_ip:
                return x_real_ip

            logger = logging.getLogger(__name__)
            logger.warning(
                "X-Real-IP header is not present. Falling back to REMOTE_ADDR")

        return self.request.META.get('REMOTE_ADDR')

    @property
    def page_number(self) -> int:
        paginator: PageNumberPagination = self.paginator
        return paginator.get_page_number(self.request, paginator)

    @property
    def page_size(self) -> int:
        paginator: PageNumberPagination = self.paginator
        return paginator.page_size

    class Meta:
        abstract = True
