from django.urls import path

from .views import (
    HomeView,
    SectionListItemView,
    ItemDetailView,
    SearchResultsView,
    CommonView,
)


app_name = "items"

urlpatterns = [
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("item/<slug>/", ItemDetailView.as_view(), name="detail_item"),
    path("section/<section>/", SectionListItemView.as_view(), name="section_list_item"),
    path(
        "section/<section>/<slug:category>",
        SectionListItemView.as_view(),
        name="section_category_list_item",
    ),
    path("info/<str:topic>/", CommonView.as_view(), name="generic_info"),
    path("", HomeView.as_view(), name="home"),
]
