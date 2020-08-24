from django.urls import path

from ..views.item import (
    HomeView,
    SectionListItemView,
    ItemDetailView,
    SearchResultsView,
    CommonView,
)
from ..views.order import (
    add_to_card,
    cart_summary,
    remove_one_from_cart,
    remove_item_from_cart,
)

from ..views.user import ProfileView

app_name = "shop"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("item/<slug>/", ItemDetailView.as_view(), name="detail_item"),
    path(
        "section/<category>/", SectionListItemView.as_view(), name="category_list_item"
    ),
    path(
        "section/<category>/<subcategory>",
        SectionListItemView.as_view(),
        name="category_subcategory_list_item",
    ),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("info/<str:topic>/", CommonView.as_view(), name="generic_info"),
    path("profile/<user>/", ProfileView.as_view(), name="profile"),
    path("add-to-cart/<slug>", add_to_card, name="add_to_cart"),
    path("add-to-cart/<slug>/<size>", add_to_card, name="add_to_cart_size"),
    path("remove-one-from-cart/<slug>", remove_one_from_cart, name="remove_one_cart"),
    path(
        "remove-one-cart-size/<slug>/<size>",
        remove_one_from_cart,
        name="remove_one_cart_size",
    ),
    path(
        "remove-item-cart-size/<slug>/",
        remove_item_from_cart,
        name="remove_item_from_cart",
    ),
    path(
        "remove-item-cart-size/<slug>/<size>",
        remove_item_from_cart,
        name="remove_item_from_cart_size",
    ),
    path("cart-summary/", cart_summary, name="cart_summary"),
]
