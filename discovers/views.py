

from django.shortcuts import get_object_or_404
from discovers.models import HomeDiscover
from django.db.models.query import QuerySet
from discovers.serializers import HomeDiscoverSerializer
from utilities.viewsets import BaseViewSet

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_flex_fields.views import FlexFieldsMixin


class HomeDiscoversViewSet(FlexFieldsMixin, BaseViewSet):
    queryset = HomeDiscover.objects.all()
    serializer_class = HomeDiscoverSerializer
    permission_classes = [permissions.AllowAny]
    permit_list_expands = []

    def list(self, request: Request) -> Response:
        """Get list of home discovers"""

        home_discovers: QuerySet = self.filter_queryset(self.get_queryset())

        # Pagination
        home_discovers = self.paginate_queryset(home_discovers)

        serializer = self.get_serializer(home_discovers, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, pk=None):
        """Get single home discover"""

        home_discover = get_object_or_404(HomeDiscover, id=pk)
        serializer = self.get_serializer(home_discover)
        return Response(serializer.data)
