from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from ..models.item import Item
from ..models.order import OrderItem, Order


def cart_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, "cart_summary.html", {"object": order})
    except ObjectDoesNotExist:
        messages.error(request, "You do not have active order")
        return redirect("/")


def add_to_card(request, slug, size=None):
    item = get_object_or_404(Item, slug=slug)
    if not size and item.category != "A":
        size = request.GET.get("size")
        if not size:
            messages.warning(request, "You have to choose size")
            return redirect("shop:detail-item", slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, item=item, ordered=False, size=size
    )
    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug, size=size).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Item quantity has been updated")
            return redirect("shop:cart-summary")
        else:
            messages.success(request, "This item has been added")
            order.items.add(order_item)
            return redirect("shop:detail-item", slug=slug)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)
        messages.success(request, "Item has been added to cart")
        return redirect("shop:detail-item", slug=slug)


def remove_one_from_cart(request, slug, size=None):
    item = get_object_or_404(Item, slug=slug)
    order_item = get_object_or_404(
        OrderItem, user=request.user, item=item, ordered=False, size=size
    )
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    if order_item.quantity > 1:
        order_item.quantity -= 1
    else:
        order.items.remove(order_item)
    order_item.save()
    messages.success(request, "Item quantity has been updated")
    return redirect("shop:cart-summary")


def remove_item_from_cart(request, slug, size=None):
    item = get_object_or_404(Item, slug=slug)
    order_item = get_object_or_404(
        OrderItem, user=request.user, item=item, ordered=False, size=size
    )
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order.items.remove(order_item)
    order.save()
    messages.success(request, "Item deleted from cart")
    return redirect("shop:cart-summary")
