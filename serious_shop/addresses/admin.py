from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Address


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "address_type",
        "email",
        "is_default",
        "order_ids",
    ]
    list_editable = ["is_default"]
    list_filter = ["is_default", "address_type"]
    search_fields = [
        "user",
        "first_name",
        "last_name",
        "email",
        "street",
        "zip_code",
        "city",
    ]

    def order_ids(self, obj):
        return ",".join(
            [str(k.id) for k in obj.shipping_address.all() | obj.billing_address.all()]
        )

    order_ids.short_description = _("ID orders")


admin.site.register(Address, AddressAdmin)
