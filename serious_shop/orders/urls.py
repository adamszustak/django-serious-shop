from django.urls import path

from .views import order_summary, confirmed_order


app_name = "orders"

urlpatterns = [
    path("order-summary/<int:order_id>", order_summary, name="order-summary"),
    path("order-confirmed/<int:order_id>", confirmed_order, name="confirmed_order"),
]
