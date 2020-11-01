from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, View

from items.models import Category, Item
from lib.models import CompanyInfo

from .filters import ItemFilter


def item_list_view(request, path=None, instance=None):
    context = {}
    if instance:
        category = Category.objects.get(id=instance.id)
        items = Item.objects.in_category(category=category)
        items_list = items.select_related("category")
        context["title"] = category.name
    elif request.GET.get("search"):
        query = request.GET.get("search")
        items_list = Item.objects.search(query).select_related("category")
    else:
        items_list = Item.objects.active().select_related("category")
        context["slider"] = True
    items_filter = ItemFilter(request.GET, queryset=items_list)
    items_list = items_filter.qs
    paginator = Paginator(items_list, 10)
    page = request.GET.get("page", 1)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context.update({"paginagor": paginator, "filter": items_filter, "items": items})
    return render(request, "home.html", context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "detail_item.html"
    queryset = Item.objects.select_related("category")

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["item_list"] = Item.objects.active().select_related("category")
        return context


class CommonView(View):
    def get(self, *args, **kwargs):
        company = CompanyInfo.objects.get(name=settings.COMPANY_NAME)
        section = self.kwargs.get("topic")
        return render(
            self.request, "generic_info.html", {"company": company, "section": section}
        )
