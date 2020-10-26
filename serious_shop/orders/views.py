from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render, reverse

from addresses.forms import BillingAddressForm, ShippingAddressForm
from addresses.models import Address
from cart.cart import Cart
from orders.models import Order, OrderItem


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0 or not cart:
        messages.warning(request, "Your cart is empty")
        return redirect("items:home")
    def_billing_address = (
        def_shipping_address
    ) = shipping_initial = billing_initial = None
    if request.user.is_authenticated:
        try:
            def_billing_address = Address.objects.default_billing(request.user)[0]
            def_shipping_address = Address.objects.default_shipping(request.user)[0]
            shipping_initial = def_shipping_address.__dict__
            billing_initial = def_billing_address.__dict__
        except (ObjectDoesNotExist, IndexError):
            pass
    if request.method == "POST":
        billing_form = BillingAddressForm(
            request.POST, prefix="billing", request=request, initial=billing_initial
        )
        shipping_form = ShippingAddressForm(
            request.POST, prefix="shipping", request=request, initial=shipping_initial
        )
        if billing_form.is_valid() and shipping_form.is_valid():
            billing = billing_form.save(commit=False)
            shipping = shipping_form.save(commit=False)
            order = Order()
            if request.user.is_authenticated:
                billing.user = shipping.user = order.user = request.user
            if def_billing_address and not billing_form.has_changed():
                order.billing_address = def_billing_address
            else:
                billing.save()
                order.billing_address = billing
            if def_shipping_address and not shipping_form.has_changed():
                order.shipping_address = def_shipping_address
            else:
                shipping.save()
                order.shipping_address = shipping
            order.session = request.session.session_key
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item["item"],
                    price=item["price"],
                    quantity=item["quantity"],
                    size=item["size"],
                )
            return redirect("payments:order_payment", order_id=order.id)
    else:
        context = {
            "cart": cart,
            "total": cart.get_final_price(),
            "shipping_form": ShippingAddressForm(
                prefix="shipping", initial=shipping_initial, request=request
            ),
            "billing_form": BillingAddressForm(
                prefix="billing", initial=billing_initial, request=request
            ),
        }
        return render(request, "checkout.html", context)
