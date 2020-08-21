from django.urls import path

from ..views.catalog import (
    HomeView,
    SectionListItemView,
    ItemDetailView,
    SearchResultsView,
    CommonView,
)
from ..views.cart import (
    add_to_card,
    cart_summary,
    remove_one_from_cart,
    remove_item_from_cart,
)

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("item/<slug>/", ItemDetailView.as_view(), name="detail-item"),
    path(
        "section/<category>/", SectionListItemView.as_view(), name="category-list-item"
    ),
    path(
        "section/<category>/<subcategory>",
        SectionListItemView.as_view(),
        name="category-subcategory-list-item",
    ),
    path("search/", SearchResultsView.as_view(), name="search-results"),
    path("info/<str:topic>/", CommonView.as_view(), name="generic-info"),
    path("add-to-cart/<slug>", add_to_card, name="add-to-cart"),
    path("add-to-cart/<slug>/<size>", add_to_card, name="add-to-cart-size"),
    path("remove-one-from-cart/<slug>", remove_one_from_cart, name="remove-one-cart"),
    path(
        "remove-one-cart-size/<slug>/<size>",
        remove_one_from_cart,
        name="remove-one-cart-size",
    ),
    path(
        "remove-item-cart-size/<slug>/",
        remove_item_from_cart,
        name="remove-item-from-cart",
    ),
    path(
        "remove-item-cart-size/<slug>/<size>",
        remove_item_from_cart,
        name="remove-item-from-cart-size",
    ),
    path("cart-summary/", cart_summary, name="cart-summary"),
]
