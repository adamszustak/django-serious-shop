from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["item"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "created_date", "show_email"]
    list_filter = ["status"]
    inlines = [OrderItemInline]

    def show_email(self, obj):
        return obj.get_email
