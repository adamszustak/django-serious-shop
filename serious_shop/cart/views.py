import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from allauth.account.decorators import verified_email_required
from allauth.account.forms import LoginForm


from items.models import Item
from .cart import Cart


def add_to_cart(request, item_id, size=None):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    if not size:
        size = request.POST.get("size") or None
    if item.is_wear and not size:
        messages.warning(request, "You need to choose size")
        return redirect("items:detail_item", slug=item.slug)
    if cart.is_in_cart(item, size) and "csrfmiddlewaretoken" not in request.POST:
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
    cart.add(item, size)
    return redirect("cart:cart_detail")


def remove_one_cart(request, item_id, size=None):
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
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty")
        return redirect("items:home")
    total = cart.get_final_price()
    return render(request, "checkout.html", {"cart": cart, "total": total})
