from rest_framework import serializers

from account.serializers import UserSerializer
from sepulka.models import Delivery, Process, Sepulka, Flow


class ProcessRetrieveSerializer(serializers.ModelSerializer):
    responsible = serializers.StringRelatedField(read_only=True,)

    class Meta:
        model = Process
        fields = (
            "is_vaccinated", "is_processed", 
            "responsible", "date_updated",
        )
        read_only_fields = fields


class ProcessResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
        read_only_fields = ("sepulka", "is_vaccinated", "is_processed")


class ProcessPropertiesSerializer(serializers.ModelSerializer):
    responsible = serializers.StringRelatedField(read_only=True,)

    class Meta:
        model = Process
        fields = "__all__"
        read_only_fields = ("sepulka", "responsible",)


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"
        read_only_fields = ("sepulka",)


class DeliveryRetrieveSerializer(serializers.ModelSerializer):
    responsible = serializers.StringRelatedField(read_only=True,)

    class Meta:
        model = Delivery
        fields = (
            "method",
            "responsible", "date_updated",
        )
        read_only_fields = fields


class SepulkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sepulka
        fields = "__all__"


class SepulkaRetrieveSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True,)

    class Meta:
        model = Sepulka
        fields = (
            "code", "name", "creator", "state",
            "is_warm", "is_square", "is_soft", "size",
        )


class SepulkaDetailRetrieveSerializer(serializers.ModelSerializer):
    process = ProcessRetrieveSerializer(read_only=True)
    delivery = DeliveryRetrieveSerializer(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Sepulka
        fields = (
            "code", "name", "creator", "state",
            "is_warm", "is_square", "is_soft", "size",
            "date_created", "date_updated",
            "process", "delivery",
        )
        read_only_fields = fields


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = "__all__"
