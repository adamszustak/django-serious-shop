import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView

from allauth.account.decorators import verified_email_required
from allauth.account.forms import LoginForm


from items.models import Item
from .cart import Cart
from addresses.forms import BillingAddressForm, ShippingAddressForm
from orders.models import OrderItem, Order
from addresses.models import Address
from lib.utils import create_order_id


def add_to_cart(request, item_id, size=None):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    if not size:
        size = request.POST.get("size") or None
    if item.category.need_sizes and not size:
        messages.warning(request, "You need to choose size")
        return redirect("items:detail_item", slug=item.slug)
    if request.is_ajax() and request.method == "POST":
        cart.add(item, size)
        item_final_price = cart.get_item_final_price(item, size)
        return JsonResponse(
            {
                "cart": cart.get_cart(),
                "item_final_price": item_final_price,
                "len_cart": len(cart),
                "final_price": cart.get_final_price(),
            },
            status=200,
        )
    elif request.method == "POST":
        cart.add(item, size)
        return redirect("cart:cart_detail")
    else:
        return redirect("items:detail_item", slug=item.slug)


def remove_one_cart(request, item_id, size=None):
    if request.is_ajax and request.method == "POST":
        cart = Cart(request)
        item = get_object_or_404(Item, id=item_id)
        quantity = cart.substract(item, size)
        item_final_price = 0
        if quantity:
            item_final_price = cart.get_item_final_price(item, size)
        return JsonResponse(
            {
                "cart": cart.get_cart(),
                "item_final_price": item_final_price,
                "len_cart": len(cart),
                "final_price": cart.get_final_price(),
            },
            status=200,
        )
    return JsonResponse({"error": ""}, status=400)


def remove_item_cart(request, item_id, size=None):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item, size)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart_summary.html", {"cart": cart})


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
            cart.clear()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item["item"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            return redirect("orders:order-summary", order_id=order.id)
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
