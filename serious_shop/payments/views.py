from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

import braintree
from cart.cart import Cart
from orders.models import Order

from .decorators import user_is_order_author
from .tasks import order_created

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@user_is_order_author
def order_payment(request, order_id):
    cart = Cart(request)
    order = get_object_or_404(
        Order.objects.prefetch_related("items", "items__item").select_related(
            "billing_address", "shipping_address"
        ),
        id=order_id,
        status="created",
    )
    total_cost = order.get_total
    if request.method == "POST":
        nonce = request.POST.get("payment_method_nonce", None)
        result = gateway.transaction.sale(
            {
                "amount": f"{total_cost:.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            order.status = "paid"
            order.braintree_id = result.transaction.id
            order.save()
            cart.clear()
            order_created.delay(order.id, order.status)
            return redirect("payments:confirmed_order", order_id=order_id)
        else:
            order.status = "unpaid"
            order.save()
            cart.clear()
            order_created.delay(order.id, order.status)
            return redirect("payments:unconfirmed_order", order_id=order_id)
    else:
        client_token = gateway.client_token.generate()
        return render(
            request,
            "order_payment.html",
            {"order": order, "client_token": client_token},
        )


@user_is_order_author
def confirmed_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, status="paid")
    context = {"order": order}
    return render(request, "confirmed_order.html", context)


@user_is_order_author
def unconfirmed_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, status="unpaid")
    context = {"order": order}
    return render(request, "unconfrimed_order.html", context)
