import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["item"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "created_date", "show_email"]
    list_filter = ["status"]
    inlines = [OrderItemInline]
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        orders = [q.id for q in queryset]
        orders = "-".join([str(order) for order in orders])
        content_disposition = f"attachment; filename=Orders {orders}.csv"
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = content_disposition
        writer = csv.writer(response, delimiter=";")
        fields = [
            field
            for field in meta.get_fields()
            if not field.many_to_many and not field.one_to_many
        ]
        writer.writerow([f"{field.verbose_name}" for field in fields])
        data = []
        for obj in queryset:
            data_row = []
            for field in fields:
                value = getattr(obj, field.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%d/%m/%Y")
                data_row.append(value)
            items = obj.items.all()
            ids = ",".join([str(item.id) for item in items])
            data_row.append(ids)
            data.append(data_row)
        writer.writerows(data)
        return response

    export_to_csv.short_description = _("Export to CSV")

    def show_email(self, obj):
        return obj.get_email
