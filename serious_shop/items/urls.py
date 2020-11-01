from django.urls import path, re_path

import mptt_urls

from .views import CommonView, ItemDetailView, item_list_view

app_name = "items"
urlpatterns = [
    path("search/", item_list_view, name="search_results"),
    path("item/<slug>/", ItemDetailView.as_view(), name="detail_item"),
    re_path(
        r"^category/(?P<path>.*)",
        mptt_urls.view(
            model="items.models.Category",
            view="items.views.item_list_view",
            slug_field="slug",
            trailing_slash=True,
        ),
        name="category_list_item",
    ),
    path("info/<str:topic>/", CommonView.as_view(), name="generic_info"),
    path("", item_list_view, name="home"),
]
