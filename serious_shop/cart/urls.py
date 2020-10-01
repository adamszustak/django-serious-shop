from django.urls import path

from .views import add_to_cart, cart_detail, remove_item_cart, remove_one_cart, checkout


app_name = "cart"

urlpatterns = [
    path("detail/", cart_detail, name="cart_detail"),
    path("add/<int:item_id>", add_to_cart, name="add_to_cart"),
    path("checkout/", checkout, name="checkout"),
    path("add-size/<int:item_id>/<str:size>", add_to_cart, name="add_to_cart_size"),
    path("remove/<int:item_id>/<str:size>", remove_item_cart, name="remove_item_cart"),
    path(
        "remove-one/<int:item_id>/<str:size>", remove_one_cart, name="remove_one_cart"
    ),
]
