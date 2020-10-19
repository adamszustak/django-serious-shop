from decimal import Decimal

from django.conf import settings

from items.models import Item


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the items
        from the database.
        """
        keys = self.cart.keys()
        cart = self.cart.copy()
        item_ids = [k.split("-")[0] for k in keys]
        items = Item.objects.filter(id__in=item_ids)
        for key in keys:
            key_id = key.split("-")[0]
            cart[str(key)]["item"] = items.get(id=key_id)
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, item, size):
        """
        Add a item to the cart or update its quantity.
        """
        item_id = str(item.id)
        key = f"{item_id}-{size}"
        if key not in self.cart:
            self.cart[key] = {
                "quantity": 1,
                "price": str(item.actual_price),
                "size": size,
            }
        else:
            if self.cart[key]["quantity"] < settings.MAX_ITEM_QUANTITY_IN_CART:
                self.cart[key]["quantity"] += 1
            else:
                self.cart[key]["quantity"] += 0
        self.save()

    def substract(self, item, size):
        """
        Remove a item from the cart or update its quantity.
        """
        item_id = str(item.id)
        quantity = 0
        key = f"{item_id}-{size}"
        if self.cart[key]["quantity"] > 1:
            self.cart[key]["quantity"] -= 1
            quantity = self.cart[key]["quantity"]
        else:
            del self.cart[key]
        self.save()
        return quantity

    def save(self):
        self.session.modified = True

    def remove(self, item, size):
        """
        Remove a item from the cart.
        """
        item_id = str(item.id)
        key = f"{item_id}-{size}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def get_item_final_price(self, item, size):
        item_id = str(item.id)
        key = f"{item_id}-{size}"
        return Decimal(self.cart[key]["price"]) * self.cart[key]["quantity"]

    def get_final_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_cart(self):
        return self.cart
