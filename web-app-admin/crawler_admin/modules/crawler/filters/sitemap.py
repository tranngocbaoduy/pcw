from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

class FilterBySitemap(admin.SimpleListFilter):
    title = _("Sitemap")
    parameter_name = "sitemap"

    def lookups(self, request, model_admin):
        return list(
            set(
                [
                    (c.sitemap.id, c.sitemap.name)
                    for c in model_admin.model.objects.all()
                ]
            )
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sitemap__id=self.value())