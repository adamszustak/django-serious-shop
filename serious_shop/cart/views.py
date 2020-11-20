import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from addresses.forms import BillingAddressForm, ShippingAddressForm
from addresses.models import Address
from allauth.account.decorators import verified_email_required
from allauth.account.forms import LoginForm
from items.models import Item
from orders.models import Order, OrderItem

from .cart import Cart


def add_to_cart(request, item_id, size=None):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    if not size:
        size = request.POST.get("size") or None
    if item.category.need_sizes and not size:
        messages.warning(request, _("You need to choose size"))
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
