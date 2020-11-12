from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from addresses.models import Address
from coupons.models import Coupon
from items.models import Item, WearSize
from lib.utils import get_sentinel_user_anonymous, get_sentinel_user_deleted

from .managers import OrderQuerySet


class Order(models.Model):
    CREATED = "created"
    PAID = "paid"
    UNPAID = "unpaid"
    SHIPPED = "shipped"
    REFUNDED = "refunded"
    ORDER_STATUS_CHOICES = (
        (CREATED, _("Created")),
        (PAID, _("Paid")),
        (UNPAID, _("Unpaid")),
        (SHIPPED, _("Shipped")),
        (REFUNDED, _("Refunded")),
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET(get_sentinel_user_deleted),
        verbose_name=_("User"),
        blank=True,
        null=True,
        default=get_sentinel_user_anonymous,
    )
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_address",
        on_delete=models.SET_NULL,
        verbose_name=_("Shipping address"),
        null=True,
    )
    billing_address = models.ForeignKey(
        Address,
        related_name="billing_address",
        on_delete=models.SET_NULL,
        verbose_name=_("Billing address"),
        null=True,
        blank=True,
    )
    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.DecimalField(
        _("Discount"), max_digits=5, decimal_places=2, blank=True, null=True, default=0,
    )
    created_date = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_date = models.DateTimeField(_("Ordered at"), auto_now=True)
    status = models.CharField(
        _("Status"), max_length=120, default="created", choices=ORDER_STATUS_CHOICES
    )
    braintree_id = models.CharField(max_length=150, blank=True)
    session = models.CharField(_("Session"), max_length=100)

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order - {self.id}"

    @property
    def get_total(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total - self.discount

    @property
    def items_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total

    @property
    def get_email(self):
        if self.user == get_sentinel_user_anonymous():
            return self.shipping_address.email
        return self.user.email

    def paid(self):
        if self.status == "paid":
            return True
        return False


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name=_("Order")
    )
    item = models.ForeignKey(
        Item,
        related_name="order_items",
        on_delete=models.CASCADE,
        verbose_name=_("Item"),
    )
    size = models.CharField(
        _("Size"), max_length=4, choices=WearSize.SIZES, blank=True, null=True
    )
    price = models.DecimalField(_("Price"), max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title} - {self.size}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                item = WearSize.objects.get(item=self.item.id, size=self.size)
            except ObjectDoesNotExist:
                item = self.item
            item.quantity = F("quantity") - self.quantity
            item.save()
        super(OrderItem, self).save(*args, **kwargs)

    def get_cost(self):
        return self.price * self.quantity
