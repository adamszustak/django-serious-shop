from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from mptt.admin import DraggableMPTTAdmin

from .forms import WearSizeForm
from .models import Category, Item, ItemImage, WearSize


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
    list_display = ["title", "category", "price", "discount_price", "active"]
    list_display_links = ["title"]
    list_editable = ["active"]
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
        ordering = ("category", "title")


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = [
        "tree_actions",
        "indented_title",
        "view_items_link",
        "related_products_cumulative_count",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ("indented_title",)

    def view_items_link(self, obj):
        count = obj.items.count()
        url = (
            reverse("admin:items_item_changelist")
            + "?"
            + urlencode({"category__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Items</a>', url, count)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(
            qs, Item, "category", "products_cumulative_count", cumulative=True
        )
        return qs

    def related_products_cumulative_count(self, obj):
        return obj.products_cumulative_count

    related_products_cumulative_count.short_description = _(
        "Related products (in total)"
    )

    view_items_link.short_description = _("Items in specific category")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
