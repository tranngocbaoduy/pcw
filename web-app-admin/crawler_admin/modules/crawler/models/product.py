import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from modules.crawler.models.utils import id_generator, id_gen, ExtractInfoIphone
from pprint import pprint

class Category(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_gen, editable=False, unique=True, max_length=12
    ) 
    name = models.CharField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '#C{} - {}'.format(self.id, self.name)

class GroupProduct(models.Model):
    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    name = models.CharField(max_length=256)
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)
    meta = models.JSONField(default=dict) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#GP{} - {}'.format(self.id, self.name)

    class Meta:
        verbose_name = _('Group Product')


class Product(models.Model): 

    id = models.CharField(
        primary_key=True, default=id_generator, editable=False, unique=True, max_length=12
    )
    base_url = models.CharField(max_length=512, default='')
    name = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    encoded_base_url = models.CharField(max_length=512) 
    price = models.CharField(max_length=100,default="",blank=True,)
    list_price = models.CharField(max_length=100,default="",blank=True,)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    group_product = models.ForeignKey(GroupProduct, on_delete=models.CASCADE, blank=True, null=True)

    meta = models.JSONField(default=dict) 
    description = models.TextField(default="", blank=True,)
    list_image = models.TextField(default="", blank=True,)

    count_update = models.IntegerField("Count Update", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '#P{} - {}'.format(self.id, self.name)

    def get_base_url(self):
        return self.base_url

    def categorize(self,): 
        base_url = self.base_url
        gen_number = ExtractInfoIphone().extract_gen_number(base_url)
        ram_size = ExtractInfoIphone().extract_ram_size(base_url) 
        is_used = ExtractInfoIphone().extract_is_used(base_url)
        if ram_size and gen_number and not is_used:
            pprint({
                'gen_number': gen_number,
                'ram_size': ram_size,
                'url': base_url,   
            })

            obj, is_created = GroupProduct.objects.get_or_create(name='{}#{}'.format(gen_number,ram_size))
            self.group_product = obj
            self.save()
                # print('[data] =>',gen_number, '\t',ram_size, '\t', is_used,'\t',i) 

        # final_data = list(sorted(final_data, key=lambda x: (x['gen_number'], x['ram_size']), reverse=True))
        # for i in final_data: 
        #     if '{}#{}'.format(i['gen_number'], i['ram_size']) not in group:
        #         group['{}#{}'.format(i['gen_number'], i['ram_size'])] = []
        #     group['{}#{}'.format(i['gen_number'], i['ram_size'])].append(i['url'])
        #     print('{} \t\t- {} - {}'.format(i['gen_number'], i['ram_size'],i['url']))  

        # for key, value in group.items():
        #     print('{}'.format(key))
        #     pprint(value)
        