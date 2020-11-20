from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

import django_filters

from .models import Item


class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ["ordering"]

    CHOICES = (
        ("low_price", _("Low Price")),
        ("high_price", _("High Price")),
        ("newest", _("Newest")),
        ("popular", _("Most Popular")),
    )
    ordering = django_filters.ChoiceFilter(
        label=_("Order By"), choices=CHOICES, method="filter_by_order"
    )

    def filter_by_order(self, queryset, name, value):
        if value == "high_price":
            exp = "-price"
        elif value == "low_price":
            exp = "price"
        elif value == "newest":
            exp = "-created_date"
        else:
            return queryset.annotate(num=Count("order_items")).order_by("-num")
        return queryset.order_by(exp)
