from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "service",
        "phone",
        "preferred_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "service", "created_at")
    search_fields = (
        "client_name",
        "phone",
        "car",
    )
    list_editable = ("status",)
    readonly_fields = ("created_at",)
# Register your models here.
