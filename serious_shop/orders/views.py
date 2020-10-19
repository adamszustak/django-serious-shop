from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .decorators import user_is_order_author
from .models import Order


@user_is_order_author
def order_summary(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items", "items__item").select_related(
            "billing_address", "shipping_address"
        ),
        id=order_id,
        status="created",
    )
    context = {"order": order}
    return render(request, "order_summary.html", context)


@user_is_order_author
def confirmed_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, status="created")
    context = {"order": order}
    return render(request, "order_confirmed.html", context)
