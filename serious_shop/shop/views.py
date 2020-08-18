from itertools import chain
from operator import attrgetter

from django.db.models import Q
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, View
from django.conf import settings

from shop.models.item import Item, Category
from shop.models.company_info import CompanyInfo


class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["slider"] = True
        context["title"] = "Best Sellers"
        return context


class SectionListItemView(ListView):
    template_name = "home.html"
    paginate_by = 10

    def get_queryset(self):
        category = self.kwargs["category"]
        category_resolve = [
            item[0] for item in Category.choices if item[1] == category.title()
        ]
        try:
            subcategory = self.kwargs["subcategory"]
        except KeyError:
            subcategory = None
        if subcategory:
            return Item.objects.filter(
                category=category_resolve[0], subcategory__name__iexact=subcategory
            )
        return Item.objects.filter(category=category_resolve[0])


class SearchResultsView(ListView):
    template_name = "home.html"
    paginate_by = 10

    def get_queryset(self):
        qs = Item.objects.all()
        query = self.request.GET.get("search")
        qs_list = qs.filter(
            Q(title__icontains=query)
            | Q(category__icontains=query)
            | Q(color__icontains=query)
        )
        return qs_list


class ItemDetailView(DetailView):
    model = Item
    template_name = "detail_item.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context["item_list"] = Item.objects.all()
        return context


class CommonView(View):
    def get(self, *args, **kwargs):
        company = CompanyInfo.objects.get(name=settings.COMPANY_NAME)
        if self.kwargs["topic"] == "delivery":
            context = {"company_info": company.delivery}
        elif self.kwargs["topic"] == "privacy":
            context = {"company_info": company.privacy}
        elif self.kwargs["topic"] == "returns":
            context = {"company_info": company.returns}
        elif self.kwargs["topic"] == "contact_us":
            context = {"company_info": company.contact_us}
        elif self.kwargs["topic"] == "jobs":
            context = {"company_info": company.jobs}
        elif self.kwargs["topic"] == "about-us":
            context = {"company_info": company.about}
        else:
            context = {"company_info": "<h1>Page not found</h1>"}
        return render(self.request, "generic_info.html", context)
