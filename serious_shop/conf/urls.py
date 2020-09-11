from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("items.urls", namespace="items")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("accounts/", include("allauth.urls")),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
