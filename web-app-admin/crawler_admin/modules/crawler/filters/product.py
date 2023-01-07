from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse
 
def get_domain(url): 
    # print('url:', url.base_url)
    o = urlparse(url)
    return str(o.netloc)
    # return '123213213'

class FilterByDomain(admin.SimpleListFilter):
    title = _("Domain filter")
    parameter_name = "base_url"

    def lookups(self, request, model_admin):  
        return list(
            set(
                [
                    # (id for filter, value for display)
                    (get_domain(c.base_url), get_domain(c.base_url))
                    for c in model_admin.model.objects.all()
                ]
            )
        ) 

    def queryset(self, request, queryset): 
        if self.value():
            return queryset.filter(base_url__contains=self.value())

