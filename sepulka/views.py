from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import permissions
from sepulka import serializers
from sepulka.models import Sepulka


class SepulkaViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Sepulka.objects.all()
    serializer_class = serializers.SepulkaSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.SepulkaRetrieveSerializer

        if self.action == "retrieve":
            return serializers.SepulkaDetailRetrieveSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        perms = super().get_permissions()

        if self.action == "create":
            return [permissions.IsShmurdikPermission(), *perms]

        if self.action == "destroy":
            return [permissions.IsShmurdikOrStaffPermission(), *perms]

        return perms

    def perform_destroy(self, instance):
        return instance.safe_delete()

    def create(self, request, *args, **kwargs):
        if request.data and isinstance(request.data, dict):
            request.data["creator"] = request.user.pk

        return super().create(request, *args, **kwargs)

    def update_related_model(self, request, instance, *args, **kwargs):
        if request.method == "OPTIONS":
            return self.options(request, *args, **kwargs)

        if request.method == "PUT":
            serializer = self.get_serializer(
                instance, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)

            serializer.save()

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

    @action(
        methods=["PUT", "OPTIONS"], detail=True,
        url_path=r"process/responsible", url_name="process-responsible",
        serializer_class=serializers.ProcessResponsibleSerializer,
        permission_classes=(
            IsAuthenticated, permissions.IsShmurdikPermission,
        ),
    )
    def set_process_responsible(self, request, *args, **kwargs):
        instance = self.get_object()

        return self.update_related_model(
            request, instance.process,
            *args, **kwargs
        )

    @action(
        methods=["PUT", "OPTIONS"], detail=True,
        url_path=r"process/conveyor", url_name="process-conveyor",
        serializer_class=serializers.ProcessPropertiesSerializer,
        permission_classes=(
            IsAuthenticated, permissions.IsGrymzikPermission,
        ),
    )
    def update_process_properties(self, request, *args, **kwargs):
        instance = self.get_object()

        return self.update_related_model(
            request, instance.process,
            *args, **kwargs,
        )

    @action(
        methods=["PUT", "OPTIONS"], detail=True,
        url_path=r"delivery", url_name="delivery",
        serializer_class=serializers.DeliveryUpdateSerializer,
        permission_classes=(
            IsAuthenticated, permissions.IsFufelnitsaPermission,
        )
    )
    def update_delivery(self, request, *args, **kwargs):
        instance = self.get_object()

        return self.update_related_model(
            request, instance.delivery,
            *args, **kwargs,
        )

    @action(
        methods=["GET", "OPTIONS"], detail=True,
        serializer_class=serializers.FlowSerializer,
    )
    def list_flow(self, request, pk=None, format=None):
        instance = self.get_object()

        if request.method == "OPTIONS":
            return self.options(request, pk=pk, format=format)

        if request.method == "GET":
            messages = instance.flow_set.all()

            page = self.paginate_queryset(messages)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
