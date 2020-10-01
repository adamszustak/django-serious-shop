from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.conf import settings

from items.models import Item, Section, Category
from lib.models import CompanyInfo


class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10
    queryset = Item.objects.active()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["slider"] = True
        context["title"] = "Best Sellers"
        return context


class SectionListItemView(ListView):
    template_name = "home.html"
    paginate_by = 10

    def get_queryset(self):
        section = self.kwargs["section"]
        section_resolve = [
            item[0] for item in Section.choices if item[1] == section.title()
        ]
        category = self.kwargs.get("category")
        if category:
            return Item.objects.in_category(section_resolve[0], category)
        return Item.objects.in_section(section_resolve[0])

    def get_context_data(self, **kwargs):
        context = super(SectionListItemView, self).get_context_data(**kwargs)
        context["section"] = self.kwargs["section"]
        context["category"] = self.kwargs.get("category")
        return context


class SearchResultsView(ListView):
    template_name = "home.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("search")
        return Item.objects.search(query)


class ItemDetailView(DetailView):
    model = Item
    template_name = "detail_item.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["item_list"] = Item.objects.active()
        return context


class CommonView(View):
    def get(self, *args, **kwargs):
        company = CompanyInfo.objects.get(name=settings.COMPANY_NAME)
        section = self.kwargs.get("topic")
        return render(
            self.request, "generic_info.html", {"company": company, "section": section}
        )
