
from django.contrib import admin, messages
from modules.crawler.models.parser import WareParser, Parser
from modules.crawler.forms.parser import ParserInlineFormSet

class ParserTabularInline(admin.TabularInline):
    model = Parser
    formset = ParserInlineFormSet
    extra = 0
