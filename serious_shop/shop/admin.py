from django.contrib import admin
from django.db.models import Q

from .models.item import SubCategory, Item, WearSize, ItemImage, WearProxy
from .models.order import OrderItem, Order
from .models.company_info import CompanyInfo
from .forms import WearSizeForm, ItemForm, WearProxyForm


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    fields = ["image"]


class WearSizeInline(admin.TabularInline):
    model = WearSize
    form = WearSizeForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 5


class WearAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "discount_price", "category"]
    list_display_links = ["title"]
    search_fields = ["title", "price", "discount_price", "category"]
    inlines = [ItemImageInline, WearSizeInline]
    exclude = ("quantity", "add_quantity")
    form = WearProxyForm

    def get_queryset(self, request):
        queryset = (
            super(WearAdmin, self)
            .get_queryset(request)
            .filter(Q(category="F") | Q(category="M"))
        )
        return queryset


class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "discount_price"]
    list_display_links = ["title"]
    search_fields = ["title", "price", "discount_price", "category"]
    inlines = [
        ItemImageInline,
    ]
    form = ItemForm

    def get_queryset(self, request):
        queryset = super(ItemAdmin, self).get_queryset(request).filter(category="A")
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = ["__str__", "ordered", "being_delivered", "transaction_id"]
    list_filter = [
        "ordered",
        "being_delivered",
    ]
    search_fields = [
        "user__email",
        "items__item__title",
    ]


admin.site.register(CompanyInfo)
# admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(SubCategory)
admin.site.register(Item, ItemAdmin)
admin.site.register(WearProxy, WearAdmin)
