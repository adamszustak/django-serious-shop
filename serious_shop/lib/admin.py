from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import CompanyInfo


class TranslatedCompanyInfoAdmin(TranslationAdmin):
    pass


admin.site.register(CompanyInfo, TranslatedCompanyInfoAdmin)
