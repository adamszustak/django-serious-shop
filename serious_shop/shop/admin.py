from django.contrib import admin
from django import forms
from django.db.models import Q
from .models.item import SubCategory, Item, WearSize, ItemImage, WearProxy
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
    inlines = [
        ItemImageInline,
    ]
    form = ItemForm

    def get_queryset(self, request):
        queryset = super(ItemAdmin, self).get_queryset(request).filter(category="A")
        return queryset


admin.site.register(CompanyInfo)
admin.site.register(SubCategory)
admin.site.register(Item, ItemAdmin)
admin.site.register(WearProxy, WearAdmin)
