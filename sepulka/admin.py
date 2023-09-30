from django.contrib import admin
from django.http.request import HttpRequest

from sepulka.models import Sepulka, Process, Delivery, Flow


class SepulkaProcessInline(admin.TabularInline):
    model = Process

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False
    
    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


class SepulkaDeliveryInline(admin.TabularInline):
    model = Delivery

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False
    
    def has_change_permission(self, *args, **kwargs) -> bool:
        return False


class SepulkaFlowInline(admin.TabularInline):
    model = Flow
    extra = 1


@admin.register(Sepulka)
class SepulkaAdmin(admin.ModelAdmin):
    inlines = [
        SepulkaProcessInline,
        SepulkaDeliveryInline,
        SepulkaFlowInline,
    ]

    list_display = ("code", "name", "state", "creator",)
    list_filter = ("state",)
    search_fields = ("name", "creator",)
    ordering = ("name", "state",)


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = (
        "sepulka", "responsible",
        "is_vaccinated", "is_processed", "date_updated",
    )
    list_filter = ("is_processed", "is_vaccinated",)
    search_fields = ("responsible",)
    ordering = ("responsible", "date_updated",)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        "sepulka", "responsible",
        "method", "date_updated",
    )
    list_filter = ("method",)
    search_fields = ("responsible",)
    ordering = ("responsible", "date_updated",)
