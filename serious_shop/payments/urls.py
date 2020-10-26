from django.urls import path

from .views import confirmed_order, order_payment, unconfirmed_order

app_name = "payments"

urlpatterns = [
    path("order-payment/<int:order_id>", order_payment, name="order_payment"),
    path("order-confirmed/<int:order_id>", confirmed_order, name="confirmed_order"),
    path(
        "order-unconfirmed/<int:order_id>", unconfirmed_order, name="unconfirmed_order"
    ),
]
