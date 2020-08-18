from django.urls import path

from ..views import (
    HomeView,
    SectionListItemView,
    ItemDetailView,
    SearchResultsView,
    CommonView,
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
]
