from django.db import models
from django.contrib.auth import get_user_model

from .item import Item, WearSize


class OrderItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=4, choices=WearSize.SIZES, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.SmallIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} - {self.size}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.item.price

    @property
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_item_price - self.get_total_discount_item_price

    @property
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price
        return self.get_total_item_price


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email} - {self.ordered_date.strftime("%m/%d/%Y %H:%M")}'

    @property
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price
        return total

    @property
    def items_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total
