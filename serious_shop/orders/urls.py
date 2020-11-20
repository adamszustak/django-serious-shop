from django.urls import path
from django.views.i18n import JavaScriptCatalog

from .views import checkout

app_name = "orders"


urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
]
