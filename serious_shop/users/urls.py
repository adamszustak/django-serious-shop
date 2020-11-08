from django.urls import path

from .views import OrderUserList, pdf

app_name = "users"

urlpatterns = [
    path("<int:order_id>/pdf/", pdf, name="pdf"),
    path("history/", OrderUserList.as_view(), name="history"),
]
