from modeltranslation.translator import TranslationOptions, register

from .models import CompanyInfo


@register(CompanyInfo)
class CategoryTranslation(TranslationOptions):
    fields = (
        "about",
        "delivery",
        "privacy",
        "returns",
        "contact_us",
        "jobs",
    )
