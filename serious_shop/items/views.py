from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from items.models import Item, Category
from lib.models import CompanyInfo


class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10
    queryset = Item.objects.active().select_related("category")

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["slider"] = True
        return context


def category_view(request, path, instance):
    category = Category.objects.get(id=instance.id)
    items = Item.objects.in_category(category=category)
    items_list = items.select_related("category")
    page = request.GET.get("page", 1)
    paginator = Paginator(items_list, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {"object_list": items, "title": category.name}
    return render(request, "home.html", context)


class SearchResultsView(ListView):
    template_name = "home.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("search")
        return Item.objects.search(query).select_related("category")


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
