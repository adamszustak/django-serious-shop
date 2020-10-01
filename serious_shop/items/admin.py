from django.contrib import admin
from django.utils.http import urlencode
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Item, WearSize, ItemImage, Section
from .forms import WearSizeForm


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
            return len(WearSize.SIZES)


class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "section", "price", "discount_price", "category"]
    list_display_links = ["title"]
    search_fields = ["title", "price", "discount_price", "category"]
    list_filter = ("active",)
    inlines = [ItemImageInline, WearSizeInline]

    """
    JS adjust fields according to given category
    """

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.5.1.min.js",
            "js/admin/admin_select.js",
        )

    class Meta:
        ordering = ("section", "title")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "view_items_link"]
    prepopulated_fields = {"slug": ("name",)}

    def view_items_link(self, obj):
        count = obj.items.count()
        url = (
            reverse("admin:items_item_changelist")
            + "?"
            + urlencode({"category__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Items</a>', url, count)

    view_items_link.short_description = "Items"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
