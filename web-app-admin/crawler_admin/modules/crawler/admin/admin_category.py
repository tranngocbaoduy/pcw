from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin, messages

from modules.crawler.models.model_brand import Brand
from modules.crawler.models.model_category import Category

admin.site.register(Brand)
admin.site.site_header = "Meteor System"
admin.site.site_title = "Meteor System"
admin.site.register(Category, DraggableMPTTAdmin)
