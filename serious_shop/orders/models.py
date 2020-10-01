# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

# from items.models import Item, WearSize


# class Order(models.Model):
#     ORDER_STATUS_CHOICES = (
#     ('created', 'Created'),
#     ('paid', 'Paid'),
#     ('shipped', 'Shipped'),
#     ('refunded', 'Refunded'),
#     )
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
#     items = models.ManyToManyField('items.Item', verbose_name=_("Items"))
#     created_date = models.DateTimeField(_("Created at"), auto_now_add=True)
#     ordered_date = models.DateTimeField(_("Ordered at"))
#     ordered = models.BooleanField(_("Ordered"), default=False)
#     status = models.CharField(_("Status"), max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
#     transaction_id = models.CharField(_("Transaction id"), max_length=100, null=True, blank=True)

#     class Meta:
#         verbose_name = _("Cart")
#         verbose_name_plural = _("Carts")

#     def __str__(self):
#         return f'{self.user.email} - {self.ordered_date.strftime("%m/%d/%Y %H:%M")}'

#     @property
#     def get_total(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.get_cost
#         return total

#     @property
#     def items_quantity(self):
#         total = 0
#         for order_item in self.items.all():
#             total += order_item.quantity
#         return total

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
#     size = models.CharField(max_length=4, choices=WearSize.SIZES, blank=True, null=True)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title} - {self.size}"

#     def get_cost(self):
#         return self.price * self.quantity
