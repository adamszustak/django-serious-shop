from django.conf import settings

from shop.models.item import Category, SubCategory
from shop.models.company_info import CompanyInfo


def get_subcategory(request):
    return {"subcategories": SubCategory.objects.all(), "request": request}


def get_categories(request):
    return {"categories": Category.choices, "request": request}


def get_company_info(request):
    return {
        "company": CompanyInfo.objects.get(name=settings.COMPANY_NAME),
        "request": request,
    }
