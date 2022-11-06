from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _


class FilterByCategory(admin.SimpleListFilter):
    title = _("Category")
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return list(
            set(
                [
                    (c.category.id, c.category.name)
                    for c in model_admin.model.objects.all()
                ]
            )
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id__exact=self.value())


class FilterByDomain(admin.SimpleListFilter):
    title = _("Domain")
    parameter_name = "domain"

    def lookups(self, request, model_admin):
        return list(
            set([(c.domain, c.domain) for c in model_admin.model.objects.all()])
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(domain__exact=self.value())


class FilterByAgency(admin.SimpleListFilter):
    title = _("Agency")
    parameter_name = "agencies"

    def lookups(self, request, model_admin):
        return [("tiki", "Tiki"), ("shopee", "Shopee"), ("donghohaitrieu", "HaiTrieu")]

    def queryset(self, request, queryset):
        if self.value():
            list_fields = [
                str(_f).split(".")[-1] for _f in queryset.model._meta.get_fields()
            ]
            if "agency" in list_fields:
                return queryset.filter(agency=self.value())
            else:
                return queryset.filter(agencies__overlap=[self.value()])


class FilterByAgencyUrl(admin.SimpleListFilter):
    title = _("Agency")
    parameter_name = "agencies"

    def lookups(self, request, model_admin):
        return [("tiki.vn", "tiki.vn"), ("shopee.vn", "shopee.vn")]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(url__contains=self.value())
