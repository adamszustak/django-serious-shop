from django.urls import path

from .views import checkout

app_name = "orders"

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
]
